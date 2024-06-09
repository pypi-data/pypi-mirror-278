import os
import sys
import datetime
import json
import requests
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import Dict, Any
from pymilvus import connections, Collection, AnnSearchRequest, RRFRanker

class Utilities:

    @staticmethod
    def connection(host, port, db_name):
        """
        Establishes a connection to the database.
        """
        try:
            return connections.connect(host=host, port=port, db_name=db_name)
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            raise

    @staticmethod
    def collection(collection_name: str = ""):
        """
        Returns a collection object for the specified collection name.
        """
        try:
            conn = Collection(name=collection_name)
            return conn
        except Exception as e:
            print(f"Failed to retrieve collection: {e}")
            raise

    @staticmethod
    def get_embeddings(url, api_key, dims, texts):
        """
        Retrieves embeddings from an external API.
        """
        headers = {
            "API-Key": api_key,
            "Content-Type": "application/json"
        }

        data = {
            "dims": dims,
            "data": [texts]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()['data']
        except requests.exceptions.RequestException as e:
            print(f"Failed to get embeddings: {e}")
            raise

    @staticmethod
    def convert_ndarray(obj):
        """
        Converts numpy ndarray to list for JSON serialization.
        """
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    @staticmethod
    def scoring(json_results):
        """
        Scores the results based on similarity and recency.
        """
        try:
            # Extract similarity scores and timestamps
            similarity_scores = [entry["distance"] for entry in json_results]
            timestamps = [entry["datetime"] for entry in json_results]

            # Normalize similarity scores (higher value indicates higher similarity)
            scaler_similarity = MinMaxScaler()
            normalized_similarity_scores = scaler_similarity.fit_transform(np.array(similarity_scores).reshape(-1, 1)).flatten()

            # Normalize timestamps (higher value indicates more recent data)
            scaler_timestamp = MinMaxScaler()
            normalized_timestamps = scaler_timestamp.fit_transform(np.array(timestamps).reshape(-1, 1)).flatten()

            # Define the weight for the timestamp
            timestamp_weight = 0.5

            # Calculate blended scores
            blended_scores = (1 - timestamp_weight) * normalized_similarity_scores + timestamp_weight * normalized_timestamps

            # Add blended scores back to the data structure
            for i, entry in enumerate(json_results):
                entry["blended_score"] = blended_scores[i]

            # Sort by blended score in descending order
            return sorted(json_results, key=lambda x: x["blended_score"], reverse=True)
        except Exception as e:
            print(f"Scoring failed: {e}")
            raise

    @staticmethod
    def ann_search(connection, data, api_key):
        """
        Performs an approximate nearest neighbor search on the collection.
        """
        try:
            requests_params = []
            coll = Utilities.collection(data['collection'])

            # Define search parameters
            search_params = {"metric_type": "L2", "params": {"ef": 200}}
            embedding = Utilities.get_embeddings("https://airiacognition.onrender.com/api/embedd", api_key, 3072, data['query'])

            for field in data['query_fields']:
                requests_params.append({
                    "data": embedding,  # Text vector data
                    "anns_field": f"{field}",  # Textual data vector field
                    "param": search_params,  # Search parameters
                    "limit": data["limit"] if data["limit"] > 0  else 10
                })

            # Perform the hybrid search
            results = coll.hybrid_search(
                reqs=[AnnSearchRequest(**params) for params in requests_params],
                rerank=RRFRanker(),
                output_fields=data["result_columns"],
                limit=data["limit"] if data["limit"] > 0 else 10
            )

            # Parse results into JSON
            json_results = []
            for result in results:
                for hit in result:
                    json_results.append({
                        "id": hit.id,
                        "distance": hit.distance,
                        "title": hit.title,
                        "description": hit.description,
                        "url": hit.url,
                        "content": hit.content,
                        "datetime": hit.datetime
                    })

            # Score and return the results
            output = Utilities.scoring(json_results)
            return output
        except Exception as e:
            print(f"ANN search failed: {e}")
            raise
