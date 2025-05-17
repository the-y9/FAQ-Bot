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
    if not isinstance(user_embedding, torch.Tensor) or not isinstance(matched_embedding, torch.Tensor):
        raise TypeError("Embeddings must be torch.Tensor objects.")
    if len(labels) != 2:
        raise ValueError("Exactly two labels are required.")

    # Normalize vectors to unit length
    user_vec = user_embedding / user_embedding.norm()
    match_vec = matched_embedding / matched_embedding.norm()

    # Choose user_vec as x-axis, project the other into 2D plane for angle
    x_axis = user_vec
    y_axis = torch.randn_like(x_axis)  # random orthogonal candidate
    y_axis -= y_axis.dot(x_axis) * x_axis  # make orthogonal to x_axis
    y_axis /= y_axis.norm()

    # Project both onto this 2D basis
    user_proj = torch.tensor([user_vec.dot(x_axis), user_vec.dot(y_axis)])
    match_proj = torch.tensor([match_vec.dot(x_axis), match_vec.dot(y_axis)])

    # Plot
    plt.figure(figsize=(6, 6))
    origin = [0, 0]
    vectors = [user_proj, match_proj]
    colors = ['blue', 'green']

    for i, vec in enumerate(vectors):
        x, y = vec
        plt.quiver(*origin, x, y, angles='xy', scale_units='xy', scale=1,
                   color=colors[i], label=labels[i])
        plt.text(x + 0.05, y + 0.05, labels[i], fontsize=11)

    # Cosine similarity
    cos_sim = torch.nn.functional.cosine_similarity(user_embedding, matched_embedding, dim=0).item()
    plt.title(f"{title}\nCosine Similarity: {cos_sim:.2f}")
    plt.xlabel("Component 1 (User-Aligned)")
    plt.ylabel("Orthogonal Component")
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
