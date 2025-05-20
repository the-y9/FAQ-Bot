# v2/viz_utils.py
import matplotlib.pyplot as plt
from typing import List
import numpy as np

def get_projections_cosine(
    user_embedding: np.ndarray,
    matched_embedding: np.ndarray,
) -> dict:
    
    if not isinstance(user_embedding, np.ndarray):
        user_embedding = np.array(user_embedding, dtype=np.float32)
    if not isinstance(matched_embedding, np.ndarray):
        matched_embedding = np.array(matched_embedding, dtype=np.float32)
    

    # Normalize vectors to unit length
    user_vec = user_embedding / np.linalg.norm(user_embedding)
    match_vec = matched_embedding / np.linalg.norm(matched_embedding)

    # Cosine similarity between normalized embeddings
    cos_sim = np.dot(user_vec, match_vec).item()
    
    # Calculate the angle in degrees from cosine similarity
    angle_deg = np.degrees(np.arccos(cos_sim))

    # Choose user_vec as x-axis, project the other into 2D plane for angle
    x_axis = user_vec
    # Vector orthogonal to x_axis
    y_axis = np.eye(len(x_axis))[1] if len(x_axis) > 1 else np.array([0.0])
    y_axis -= y_axis.dot(x_axis) * x_axis  # make orthogonal
    y_axis /= np.linalg.norm(y_axis)  # normalize

    # Project vectors onto this 2D basis
    user_proj = np.array([user_vec.dot(x_axis), user_vec.dot(y_axis)])
    match_proj = np.array([match_vec.dot(x_axis), match_vec.dot(y_axis)])

    # Rotate user_proj by angle_deg to get a new vector
    angle_rad = np.radians(angle_deg)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ], dtype=np.float32)

    rotated_vec = np.matmul(rotation_matrix, user_proj)
    # 🔄 Rescale rotated vector to match match_proj's norm
    rotated_vec = rotated_vec / np.linalg.norm(rotated_vec) * np.linalg.norm(match_proj)

    return {"user_proj": user_proj.tolist(), 
            "match_proj": match_proj.tolist(), 
            "rotated_vec": rotated_vec.tolist(), 
            "cos_sim": cos_sim, 
            "angle_deg": angle_deg}

def plot_embeddings_cosine(
        labels: List[str], 
        user_proj: np.ndarray,
        rotated_vec: np.ndarray,
        cos_sim: float,
        angle_deg: float,
        title: str = "Cosine-Based Embedding Visualization") -> plt.Figure:
    
    if len(labels) != 2:
        raise ValueError("Exactly two labels are required.")
    # Plot
    fig, ax = plt.subplots()
    ax.quiver(0, 0, user_proj[0], user_proj[1], angles='xy', scale_units='xy', scale=1, color='blue', label=labels[0])
    ax.quiver(0, 0, rotated_vec[0], rotated_vec[1], angles='xy', scale_units='xy', scale=1, color='red', label=labels[1])
    ax.annotate(labels[1], (rotated_vec[0], rotated_vec[1]), fontsize=11, color='red', textcoords="offset points", xytext=(5,5))
    ax.annotate(labels[0], (user_proj[0], user_proj[1]), fontsize=11, color='blue', textcoords="offset points", xytext=(5,5))

    # Set title with cosine similarity and angle
    ax.set_title(f"{title}\nCosine Similarity: {cos_sim:.2f} (~{angle_deg:.2f}°)")
    ax.set_xlabel("Component 1 (User-Aligned)")
    ax.set_ylabel("Orthogonal Component")
    ax.grid(True)
    ax.legend()

    # Dynamically adjust x and y limits based on the vectors' magnitude
    margin = 0.2  # Add some margin for visualization
    ax.set_xlim(- margin, 1 + margin)
    ax.set_ylim(- margin, 1 + margin)

    # Ensure equal scaling on both axes
    ax.set_aspect('equal')

    plt.tight_layout()
    # plt.show()

    return fig
