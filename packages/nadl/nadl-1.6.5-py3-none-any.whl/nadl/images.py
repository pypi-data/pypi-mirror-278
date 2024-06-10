#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""Python ♡ Nasy.

    |             *         *
    |                  .                .
    |           .                              登
    |     *                      ,
    |                   .                      至
    |
    |                               *          恖
    |          |\___/|
    |          )    -(             .           聖 ·
    |         =\ -   /=
    |           )===(       *
    |          /   - \
    |          |-    |
    |         /   -   \     0.|.0
    |  NASY___\__( (__/_____(\=/)__+1s____________
    |  ______|____) )______|______|______|______|_
    |  ___|______( (____|______|______|______|____
    |  ______|____\_|______|______|______|______|_
    |  ___|______|______|______|______|______|____
    |  ______|______|______|______|______|______|_
    |  ___|______|______|______|______|______|____

author   : Nasy https://nasy.moe
date     : Apr 26, 2024
email    : Nasy <nasyxx+python@gmail.com>
filename : images.py
project  : nadl
license  : GPL-3.0+

Images related utilities.
"""

import jax
import jax.numpy as jnp
from jaxtyping import Float, Array, Integer


def make_patches(
  image: Float[Array, "h w c"] | Integer[Array, "h w c"],
  patch_sizes: tuple[int, int],
  stride_sizes: tuple[int, int],
) -> jax.Array:
  """Extract patches from an input image."""
  image = jnp.asarray(image)

  # Unpack patch and stride sizes
  patch_height, patch_width = patch_sizes
  stride_height, stride_width = stride_sizes

  # Image dimensions
  img_height, img_width, _ = image.shape

  # Compute number of patches along each dimension
  num_patches_height = (img_height - patch_height) // stride_height + 1
  num_patches_width = (img_width - patch_width) // stride_width + 1

  # Creating patch index grid
  i, j = jnp.meshgrid(
    jnp.arange(num_patches_height) * stride_height,
    jnp.arange(num_patches_width) * stride_width,
    indexing="ij",
  )

  # Extract patches using advanced indexing
  return image[
    i[:, :, None, None] + jnp.arange(patch_height)[None, None, :, None],
    j[:, :, None, None] + jnp.arange(patch_width)[None, None, None, :],
    None,
  ]
