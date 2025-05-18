import matplotlib.pyplot as plt
import torch
from typing import List

def visualize_embeddings_cosine(
    user_embedding: torch.Tensor,
    matched_embedding: torch.Tensor,
    labels: List[str],
    title: str = "Cosine-Based Embedding Visualization"
) -> None:
    """
    Visualizes two high-dimensional embeddings as normalized 2D vectors using cosine similarity alignment.
    """
    # Input validation
    if not isinstance(user_embedding, torch.Tensor) or not isinstance(matched_embedding, torch.Tensor):
        raise TypeError("Embeddings must be torch.Tensor objects.")
    if len(labels) != 2:
        raise ValueError("Exactly two labels are required.")

    # Normalize vectors to unit length
    user_vec = user_embedding / user_embedding.norm()
    match_vec = matched_embedding / matched_embedding.norm()

    # Choose user_vec as x-axis, project the other into 2D plane for angle
    x_axis = user_vec
    # Random vector orthogonal to x_axis
    y_axis = torch.randn_like(x_axis)  
    y_axis -= y_axis.dot(x_axis) * x_axis  # make orthogonal
    y_axis /= y_axis.norm()  # normalize

    # Project vectors onto this 2D basis
    user_proj = torch.tensor([user_vec.dot(x_axis), user_vec.dot(y_axis)])
    match_proj = torch.tensor([match_vec.dot(x_axis), match_vec.dot(y_axis)])

    # Cosine similarity between normalized embeddings
    cos_sim = torch.dot(user_vec, match_vec).item()

    # Plot
    fig, ax = plt.subplots()
    ax.quiver(0, 0, user_proj[0], user_proj[1], angles='xy', scale_units='xy', scale=1, color='blue', label=labels[0])
    ax.quiver(0, 0, match_proj[0], match_proj[1], angles='xy', scale_units='xy', scale=1, color='green', label=labels[1])

    # Annotate labels
    ax.annotate(labels[0], (user_proj[0], user_proj[1]), fontsize=11, color='blue', textcoords="offset points", xytext=(5,5))
    ax.annotate(labels[1], (match_proj[0], match_proj[1]), fontsize=11, color='green', textcoords="offset points", xytext=(5,5))

    # Set title with cosine similarity
    ax.set_title(f"{title}\nCosine Similarity: {cos_sim:.2f}")
    ax.set_xlabel("Component 1 (User-Aligned)")
    ax.set_ylabel("Orthogonal Component")
    ax.grid(True)
    ax.legend()
 # Dynamically adjust x and y limits based on the vectors' magnitude
    max_magnitude = max(user_proj.norm().item(), match_proj.norm().item())  # Find max vector magnitude
    margin = 0.2  # Add some margin for visualization
    ax.set_xlim(-max_magnitude - margin, max_magnitude + margin)
    ax.set_ylim(-max_magnitude - margin, max_magnitude + margin)

    # Ensure equal scaling on both axes
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.show()
