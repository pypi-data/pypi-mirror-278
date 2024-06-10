"""
Color manipulations for pyAgrum.lib module
"""

# (c) Copyright 2015-2023 by Pierre-Henri Wuillemin(@LIP6)
# (pierre-henri.wuillemin@lip6.fr)

# Permission to use, copy, modify, and distribute this
# software and its documentation for any purpose and
# without fee or royalty is hereby granted, provided
# that the above copyright notice appear in all copies
# and that both that copyright notice and this permission
# notice appear in supporting documentation or portions
# thereof, including modifications, that you make.

# THE AUTHOR P.H. WUILLEMIN  DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
# RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOFTWARE!
from typing import List, Tuple

import matplotlib as mpl
import matplotlib.colors

import pyAgrum as gum
from pyAgrum.lib.utils import getBlackInTheme


def hex2rgb(vstr: str) -> List[int]:
  """
  from "#FFFFFF" to [255,255,255]

  Parameters
  ----------
  vstr: str
    the rbg string
  Returns
  -------
  List[int]
    the list [r,g,b]
  """
  value = vstr.lstrip('#')
  lv = len(value)
  return [int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)]


def hextuple2rgb(vtuple: List[str]) -> List[int]:
  """
  from ("FF","FF","FF") to [255,255,255]

  Parameters
  ----------
  vtuple : Tuple[str,str,str]
    the Tuple of hexa values

  Returns
  -------
  List[int,int,int]
    the list [r,g,b]
  """
  return [int(v, 16) for v in vtuple]


def rgb2brightness(r: int, g: int, b: int) -> str:
  """
  Give the fgcol for a background (r,g,b).

  Parameters
  ----------
  g: int[0,255]
  r: int[0,255]
  b: int[0,255]

  Returns
  -------
  str
    "white" or "black"
  """
  brightness = r * 0.299 + g * 0.587 + b * 0.114
  return "white" if brightness <= 153 else "black"


def proba2hex(p: float, cmap: matplotlib.colors.Colormap, withSpecialColor: bool) -> Tuple[str, str, str]:
  """
  From a proba p and cmap gives the HTML rgb color

  Parameters
  ----------
  p: float
    the proba
  cmap: matplotlib.colors.Colormap
    the cmap
  withSpecialColor: bool
    do we have special colors for p=0 or 1 ?

  Returns
  -------
  Tuple(str,str,str)
    the hex values for r,g,b.
  """
  if withSpecialColor:  # add special color for p=0 or p=1
    if p == 0.0:
      return "FF", "33", "33"
    elif p == 1.0:
      return "AA", "FF", "FF"

  a, b, c, _ = cmap(p)
  return f"{int(a * 256):02x}", f"{int(b * 256):02x}", f"{int(c * 256):02x}"


def proba2color(p: float, cmap: matplotlib.colors.Colormap) -> str:
  """
  From a proba p and cmap gives the HTML rgb color

  Parameters
  ----------
  p: float
    a value in [0,1]
  cmap: matplotlib.colors.Colormap

  Returns
  -------
  str
    the html representation of the color
  """
  r, g, b = proba2hex(p, cmap, withSpecialColor=False)
  return "#" + r + g + b


def proba2bgcolor(p: float, cmap: matplotlib.colors.Colormap) -> str:
  """
  From a proba p and cmap gives the HTML rgb color (with special colors for p=0 and p=1)

  Parameters
  ----------
  p: float
    a value in [0,1]
  cmap: matplotlib.colors.Colormap

  Returns
  -------
  str
    the html representation of the background color
  """
  r, g, b = proba2hex(p, cmap, withSpecialColor=True)
  return "#" + r + g + b


def proba2fgcolor(p: float, cmap: matplotlib.colors.Colormap) -> str:
  """
  From a proba p and cmap, returns the best choice for text color for the bgcolor(p,cmap).

  Parameters
  ----------
  p: float
    a value in [0,1]
  cmap: matplotlib.colors.Colormap

  Returns
  -------
  str
    the html representation of the foreground color
  """
  a, b, c = hextuple2rgb(list(proba2hex(p, cmap, withSpecialColor=True)))
  return rgb2brightness(a, b, c)


def fontFromMatplotlib():
  """
  Find the font name and the font size ysed by matplotlib

  Returns
  -------
    fontname,size : font name and size from matplotlib
  """
  family = mpl.rcParams['font.family'][0]
  if family == "sans-serif":
    family = mpl.rcParams['font.sans-serif'][0]
  return family, mpl.rcParams['font.size']


def prepareDot(dotgraph, **kwargs):
  if "size" in kwargs and kwargs["size"] is not None:
    dotgraph.set_size(kwargs["size"])

  # workaround for some badly parsed graph (pyparsing>=3.03)
  dotgraph.del_node('"\\n"')
  dotgraph.del_node('"\\n\\n"')

  if dotgraph.get_rankdir() is None:
    dotgraph.set_rankdir(gum.config["notebook", "graph_rankdir"])
  if dotgraph.get_layout() is None:
    dotgraph.set_layout(gum.config["notebook", "graph_layout"])

  dotgraph.set_bgcolor("transparent")
  for e in dotgraph.get_edges():
    if e.get_color() is None:
      e.set_color(getBlackInTheme())
  for n in dotgraph.get_nodes():
    if n.get_color() is None:
      n.set_color(getBlackInTheme())
    if n.get_fontcolor() is None:
      n.set_fontcolor(getBlackInTheme())

  return dotgraph
