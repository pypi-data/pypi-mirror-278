# pylint: disable=too-many-branches,too-many-statements,too-many-locals
#   All three of these Pylint exceptions are because this module is basically
#   one top-to-bottom procedure.
"""
Smash xbar client.  Displays status in format usable for [xbar](xbarapp.com).
"""
from datetime import datetime
import requests
from smash import config
from smash import smash
from smash import status
from smash.status import State
from smash import version


# TODO: get smash command from install
SMASH_CMD = '/usr/local/bin/smash'

state_colours = {
    'okay': 'green',
    'unknown': 'gray',
    'warning': 'orange',
    'error': 'red',
    'unusable': 'black',
    'stale': 'brown',
    'acknowledged': 'blue'
}

# pylint: disable=line-too-long
state_icons = {
    'okay': 'iVBORw0KGgoAAAANSUhEUgAAABoAAAAWCAYAAADeiIy1AAAEDmlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPpu5syskzoPUpqaSDv41lLRsUtGE2uj+ZbNt3CyTbLRBkMns3Z1pJjPj/KRpKT4UQRDBqOCT4P9bwSchaqvtiy2itFCiBIMo+ND6R6HSFwnruTOzu5O4a73L3PnmnO9+595z7t4LkLgsW5beJQIsGq4t5dPis8fmxMQ6dMF90A190C0rjpUqlSYBG+PCv9rt7yDG3tf2t/f/Z+uuUEcBiN2F2Kw4yiLiZQD+FcWyXYAEQfvICddi+AnEO2ycIOISw7UAVxieD/Cyz5mRMohfRSwoqoz+xNuIB+cj9loEB3Pw2448NaitKSLLRck2q5pOI9O9g/t/tkXda8Tbg0+PszB9FN8DuPaXKnKW4YcQn1Xk3HSIry5ps8UQ/2W5aQnxIwBdu7yFcgrxPsRjVXu8HOh0qao30cArp9SZZxDfg3h1wTzKxu5E/LUxX5wKdX5SnAzmDx4A4OIqLbB69yMesE1pKojLjVdoNsfyiPi45hZmAn3uLWdpOtfQOaVmikEs7ovj8hFWpz7EV6mel0L9Xy23FMYlPYZenAx0yDB1/PX6dledmQjikjkXCxqMJS9WtfFCyH9XtSekEF+2dH+P4tzITduTygGfv58a5VCTH5PtXD7EFZiNyUDBhHnsFTBgE0SQIA9pfFtgo6cKGuhooeilaKH41eDs38Ip+f4At1Rq/sjr6NEwQqb/I/DQqsLvaFUjvAx+eWirddAJZnAj1DFJL0mSg/gcIpPkMBkhoyCSJ8lTZIxk0TpKDjXHliJzZPO50dR5ASNSnzeLvIvod0HG/mdkmOC0z8VKnzcQ2M/Yz2vKldduXjp9bleLu0ZWn7vWc+l0JGcaai10yNrUnXLP/8Jf59ewX+c3Wgz+B34Df+vbVrc16zTMVgp9um9bxEfzPU5kPqUtVWxhs6OiWTVW+gIfywB9uXi7CGcGW/zk98k/kmvJ95IfJn/j3uQ+4c5zn3Kfcd+AyF3gLnJfcl9xH3OfR2rUee80a+6vo7EK5mmXUdyfQlrYLTwoZIU9wsPCZEtP6BWGhAlhL3p2N6sTjRdduwbHsG9kq32sgBepc+xurLPW4T9URpYGJ3ym4+8zA05u44QjST8ZIoVtu3qE7fWmdn5LPdqvgcZz8Ww8BWJ8X3w0PhQ/wnCDGd+LvlHs8dRy6bLLDuKMaZ20tZrqisPJ5ONiCq8yKhYM5cCgKOu66Lsc0aYOtZdo5QCwezI4wm9J/v0X23mlZXOfBjj8Jzv3WrY5D+CsA9D7aMs2gGfjve8ArD6mePZSeCfEYt8CONWDw8FXTxrPqx/r9Vt4biXeANh8vV7/+/16ffMD1N8AuKD/A/8leAvFY9bLAAAAOGVYSWZNTQAqAAAACAABh2kABAAAAAEAAAAaAAAAAAACoAIABAAAAAEAAAAaoAMABAAAAAEAAAAWAAAAAKrxeTEAAACHSURBVEgN7ZTBCsAwCEO7sf//5Q0vopCIiocd7MmqeWmF9pxdzQlcQPeCXCeF2MqZMhEgZdGCHqMeKPMJtNoU9KBSODIRWLCNESzKWa3Gd6SYrK1Re5o7uv+Pjv0M8rr1sRWvAX8GZiRsKCia0vbuLRDQsdCpXQMiJHOO7TYEkDXOsIjFYPoDLQIPGOpd4jAAAAAASUVORK5CYII=',
    'unknown': 'iVBORw0KGgoAAAANSUhEUgAAABoAAAAWCAYAAADeiIy1AAAEDmlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPpu5syskzoPUpqaSDv41lLRsUtGE2uj+ZbNt3CyTbLRBkMns3Z1pJjPj/KRpKT4UQRDBqOCT4P9bwSchaqvtiy2itFCiBIMo+ND6R6HSFwnruTOzu5O4a73L3PnmnO9+595z7t4LkLgsW5beJQIsGq4t5dPis8fmxMQ6dMF90A190C0rjpUqlSYBG+PCv9rt7yDG3tf2t/f/Z+uuUEcBiN2F2Kw4yiLiZQD+FcWyXYAEQfvICddi+AnEO2ycIOISw7UAVxieD/Cyz5mRMohfRSwoqoz+xNuIB+cj9loEB3Pw2448NaitKSLLRck2q5pOI9O9g/t/tkXda8Tbg0+PszB9FN8DuPaXKnKW4YcQn1Xk3HSIry5ps8UQ/2W5aQnxIwBdu7yFcgrxPsRjVXu8HOh0qao30cArp9SZZxDfg3h1wTzKxu5E/LUxX5wKdX5SnAzmDx4A4OIqLbB69yMesE1pKojLjVdoNsfyiPi45hZmAn3uLWdpOtfQOaVmikEs7ovj8hFWpz7EV6mel0L9Xy23FMYlPYZenAx0yDB1/PX6dledmQjikjkXCxqMJS9WtfFCyH9XtSekEF+2dH+P4tzITduTygGfv58a5VCTH5PtXD7EFZiNyUDBhHnsFTBgE0SQIA9pfFtgo6cKGuhooeilaKH41eDs38Ip+f4At1Rq/sjr6NEwQqb/I/DQqsLvaFUjvAx+eWirddAJZnAj1DFJL0mSg/gcIpPkMBkhoyCSJ8lTZIxk0TpKDjXHliJzZPO50dR5ASNSnzeLvIvod0HG/mdkmOC0z8VKnzcQ2M/Yz2vKldduXjp9bleLu0ZWn7vWc+l0JGcaai10yNrUnXLP/8Jf59ewX+c3Wgz+B34Df+vbVrc16zTMVgp9um9bxEfzPU5kPqUtVWxhs6OiWTVW+gIfywB9uXi7CGcGW/zk98k/kmvJ95IfJn/j3uQ+4c5zn3Kfcd+AyF3gLnJfcl9xH3OfR2rUee80a+6vo7EK5mmXUdyfQlrYLTwoZIU9wsPCZEtP6BWGhAlhL3p2N6sTjRdduwbHsG9kq32sgBepc+xurLPW4T9URpYGJ3ym4+8zA05u44QjST8ZIoVtu3qE7fWmdn5LPdqvgcZz8Ww8BWJ8X3w0PhQ/wnCDGd+LvlHs8dRy6bLLDuKMaZ20tZrqisPJ5ONiCq8yKhYM5cCgKOu66Lsc0aYOtZdo5QCwezI4wm9J/v0X23mlZXOfBjj8Jzv3WrY5D+CsA9D7aMs2gGfjve8ArD6mePZSeCfEYt8CONWDw8FXTxrPqx/r9Vt4biXeANh8vV7/+/16ffMD1N8AuKD/A/8leAvFY9bLAAAAOGVYSWZNTQAqAAAACAABh2kABAAAAAEAAAAaAAAAAAACoAIABAAAAAEAAAAaoAMABAAAAAEAAAAWAAAAAKrxeTEAAACxSURBVEgN7ZJRDoAwCEOn8f5XVkkGYVoQcP7pzzZGX8tia/9XfIEF6HZQq5QQWzizTAhosswLiZHfCHNztNLk9KAr98lIoMF6j2BeTWtl701kwUR8NjymZ0jWiEw0/Hpm7m1db5WPClmj0jSUPWvE84afjAVVIz0Zs9y1aqT/PNeAL6tG6Yms35tA6dQ9PQxhGZEGCjrs9VKdAhkPLJR6aECEYG1gDwcDEDWOsAyLieUDSQQVHoZVdUkAAAAASUVORK5CYII=',
    'warning': 'iVBORw0KGgoAAAANSUhEUgAAABoAAAAWCAYAAADeiIy1AAAEDmlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPpu5syskzoPUpqaSDv41lLRsUtGE2uj+ZbNt3CyTbLRBkMns3Z1pJjPj/KRpKT4UQRDBqOCT4P9bwSchaqvtiy2itFCiBIMo+ND6R6HSFwnruTOzu5O4a73L3PnmnO9+595z7t4LkLgsW5beJQIsGq4t5dPis8fmxMQ6dMF90A190C0rjpUqlSYBG+PCv9rt7yDG3tf2t/f/Z+uuUEcBiN2F2Kw4yiLiZQD+FcWyXYAEQfvICddi+AnEO2ycIOISw7UAVxieD/Cyz5mRMohfRSwoqoz+xNuIB+cj9loEB3Pw2448NaitKSLLRck2q5pOI9O9g/t/tkXda8Tbg0+PszB9FN8DuPaXKnKW4YcQn1Xk3HSIry5ps8UQ/2W5aQnxIwBdu7yFcgrxPsRjVXu8HOh0qao30cArp9SZZxDfg3h1wTzKxu5E/LUxX5wKdX5SnAzmDx4A4OIqLbB69yMesE1pKojLjVdoNsfyiPi45hZmAn3uLWdpOtfQOaVmikEs7ovj8hFWpz7EV6mel0L9Xy23FMYlPYZenAx0yDB1/PX6dledmQjikjkXCxqMJS9WtfFCyH9XtSekEF+2dH+P4tzITduTygGfv58a5VCTH5PtXD7EFZiNyUDBhHnsFTBgE0SQIA9pfFtgo6cKGuhooeilaKH41eDs38Ip+f4At1Rq/sjr6NEwQqb/I/DQqsLvaFUjvAx+eWirddAJZnAj1DFJL0mSg/gcIpPkMBkhoyCSJ8lTZIxk0TpKDjXHliJzZPO50dR5ASNSnzeLvIvod0HG/mdkmOC0z8VKnzcQ2M/Yz2vKldduXjp9bleLu0ZWn7vWc+l0JGcaai10yNrUnXLP/8Jf59ewX+c3Wgz+B34Df+vbVrc16zTMVgp9um9bxEfzPU5kPqUtVWxhs6OiWTVW+gIfywB9uXi7CGcGW/zk98k/kmvJ95IfJn/j3uQ+4c5zn3Kfcd+AyF3gLnJfcl9xH3OfR2rUee80a+6vo7EK5mmXUdyfQlrYLTwoZIU9wsPCZEtP6BWGhAlhL3p2N6sTjRdduwbHsG9kq32sgBepc+xurLPW4T9URpYGJ3ym4+8zA05u44QjST8ZIoVtu3qE7fWmdn5LPdqvgcZz8Ww8BWJ8X3w0PhQ/wnCDGd+LvlHs8dRy6bLLDuKMaZ20tZrqisPJ5ONiCq8yKhYM5cCgKOu66Lsc0aYOtZdo5QCwezI4wm9J/v0X23mlZXOfBjj8Jzv3WrY5D+CsA9D7aMs2gGfjve8ArD6mePZSeCfEYt8CONWDw8FXTxrPqx/r9Vt4biXeANh8vV7/+/16ffMD1N8AuKD/A/8leAvFY9bLAAAAOGVYSWZNTQAqAAAACAABh2kABAAAAAEAAAAaAAAAAAACoAIABAAAAAEAAAAaoAMABAAAAAEAAAAWAAAAAKrxeTEAAAC1SURBVEgN7ZLBEoAgCESt6f9/uYaDDDjLimS3uoQI+xa1tf8rnsAB+m6Qq6SQtursgohgqBVuqI31QDUv0qtFpAZt0SOTBits43EPiduc7dX4tBVfxlmQHIe6qxjKgkT7FYw9BmScXTSdeGUiBO45gYiJ0MgOUId0KPxnQPRI2BSWOAOl3FrBKI4eg31hs4lGbXhPEUiaYcOoWl2vumccp4VcuwKmNNlz2m4RNGbBGa0AsTH9AMKGGBn+BQpLAAAAAElFTkSuQmCC',
    'error': 'iVBORw0KGgoAAAANSUhEUgAAABoAAAAWCAYAAADeiIy1AAAEDmlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPpu5syskzoPUpqaSDv41lLRsUtGE2uj+ZbNt3CyTbLRBkMns3Z1pJjPj/KRpKT4UQRDBqOCT4P9bwSchaqvtiy2itFCiBIMo+ND6R6HSFwnruTOzu5O4a73L3PnmnO9+595z7t4LkLgsW5beJQIsGq4t5dPis8fmxMQ6dMF90A190C0rjpUqlSYBG+PCv9rt7yDG3tf2t/f/Z+uuUEcBiN2F2Kw4yiLiZQD+FcWyXYAEQfvICddi+AnEO2ycIOISw7UAVxieD/Cyz5mRMohfRSwoqoz+xNuIB+cj9loEB3Pw2448NaitKSLLRck2q5pOI9O9g/t/tkXda8Tbg0+PszB9FN8DuPaXKnKW4YcQn1Xk3HSIry5ps8UQ/2W5aQnxIwBdu7yFcgrxPsRjVXu8HOh0qao30cArp9SZZxDfg3h1wTzKxu5E/LUxX5wKdX5SnAzmDx4A4OIqLbB69yMesE1pKojLjVdoNsfyiPi45hZmAn3uLWdpOtfQOaVmikEs7ovj8hFWpz7EV6mel0L9Xy23FMYlPYZenAx0yDB1/PX6dledmQjikjkXCxqMJS9WtfFCyH9XtSekEF+2dH+P4tzITduTygGfv58a5VCTH5PtXD7EFZiNyUDBhHnsFTBgE0SQIA9pfFtgo6cKGuhooeilaKH41eDs38Ip+f4At1Rq/sjr6NEwQqb/I/DQqsLvaFUjvAx+eWirddAJZnAj1DFJL0mSg/gcIpPkMBkhoyCSJ8lTZIxk0TpKDjXHliJzZPO50dR5ASNSnzeLvIvod0HG/mdkmOC0z8VKnzcQ2M/Yz2vKldduXjp9bleLu0ZWn7vWc+l0JGcaai10yNrUnXLP/8Jf59ewX+c3Wgz+B34Df+vbVrc16zTMVgp9um9bxEfzPU5kPqUtVWxhs6OiWTVW+gIfywB9uXi7CGcGW/zk98k/kmvJ95IfJn/j3uQ+4c5zn3Kfcd+AyF3gLnJfcl9xH3OfR2rUee80a+6vo7EK5mmXUdyfQlrYLTwoZIU9wsPCZEtP6BWGhAlhL3p2N6sTjRdduwbHsG9kq32sgBepc+xurLPW4T9URpYGJ3ym4+8zA05u44QjST8ZIoVtu3qE7fWmdn5LPdqvgcZz8Ww8BWJ8X3w0PhQ/wnCDGd+LvlHs8dRy6bLLDuKMaZ20tZrqisPJ5ONiCq8yKhYM5cCgKOu66Lsc0aYOtZdo5QCwezI4wm9J/v0X23mlZXOfBjj8Jzv3WrY5D+CsA9D7aMs2gGfjve8ArD6mePZSeCfEYt8CONWDw8FXTxrPqx/r9Vt4biXeANh8vV7/+/16ffMD1N8AuKD/A/8leAvFY9bLAAAAOGVYSWZNTQAqAAAACAABh2kABAAAAAEAAAAaAAAAAAACoAIABAAAAAEAAAAaoAMABAAAAAEAAAAWAAAAAKrxeTEAAADESURBVEgN7ZLbDsMwCEPTaf//y52QGgTIJk7Ux+2l4eJjQBvj/zu8wAV0N8idpBDbOW+ZGJCyaMHH2H8489tovanpQaX2ZCaIYPZG4JqD2k/tEmIDRZggGUMxslNsg6u7YmSa5d0ruMbdn6H2ruJ26xMjtJ2ZzDw0VE8XtzFQhEWT2JfeilGEJvETzE1QzXOr06FpJbA7PA9mZLC5yfxWLYvhIMzIIFDA6Lv53ek7fmKhqVNDR1rUEjsFRKgaKyxi8WL6B9bbHBnLeCTIAAAAAElFTkSuQmCC',
    'unusable': 'iVBORw0KGgoAAAANSUhEUgAAABoAAAAWCAYAAADeiIy1AAAEDmlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPpu5syskzoPUpqaSDv41lLRsUtGE2uj+ZbNt3CyTbLRBkMns3Z1pJjPj/KRpKT4UQRDBqOCT4P9bwSchaqvtiy2itFCiBIMo+ND6R6HSFwnruTOzu5O4a73L3PnmnO9+595z7t4LkLgsW5beJQIsGq4t5dPis8fmxMQ6dMF90A190C0rjpUqlSYBG+PCv9rt7yDG3tf2t/f/Z+uuUEcBiN2F2Kw4yiLiZQD+FcWyXYAEQfvICddi+AnEO2ycIOISw7UAVxieD/Cyz5mRMohfRSwoqoz+xNuIB+cj9loEB3Pw2448NaitKSLLRck2q5pOI9O9g/t/tkXda8Tbg0+PszB9FN8DuPaXKnKW4YcQn1Xk3HSIry5ps8UQ/2W5aQnxIwBdu7yFcgrxPsRjVXu8HOh0qao30cArp9SZZxDfg3h1wTzKxu5E/LUxX5wKdX5SnAzmDx4A4OIqLbB69yMesE1pKojLjVdoNsfyiPi45hZmAn3uLWdpOtfQOaVmikEs7ovj8hFWpz7EV6mel0L9Xy23FMYlPYZenAx0yDB1/PX6dledmQjikjkXCxqMJS9WtfFCyH9XtSekEF+2dH+P4tzITduTygGfv58a5VCTH5PtXD7EFZiNyUDBhHnsFTBgE0SQIA9pfFtgo6cKGuhooeilaKH41eDs38Ip+f4At1Rq/sjr6NEwQqb/I/DQqsLvaFUjvAx+eWirddAJZnAj1DFJL0mSg/gcIpPkMBkhoyCSJ8lTZIxk0TpKDjXHliJzZPO50dR5ASNSnzeLvIvod0HG/mdkmOC0z8VKnzcQ2M/Yz2vKldduXjp9bleLu0ZWn7vWc+l0JGcaai10yNrUnXLP/8Jf59ewX+c3Wgz+B34Df+vbVrc16zTMVgp9um9bxEfzPU5kPqUtVWxhs6OiWTVW+gIfywB9uXi7CGcGW/zk98k/kmvJ95IfJn/j3uQ+4c5zn3Kfcd+AyF3gLnJfcl9xH3OfR2rUee80a+6vo7EK5mmXUdyfQlrYLTwoZIU9wsPCZEtP6BWGhAlhL3p2N6sTjRdduwbHsG9kq32sgBepc+xurLPW4T9URpYGJ3ym4+8zA05u44QjST8ZIoVtu3qE7fWmdn5LPdqvgcZz8Ww8BWJ8X3w0PhQ/wnCDGd+LvlHs8dRy6bLLDuKMaZ20tZrqisPJ5ONiCq8yKhYM5cCgKOu66Lsc0aYOtZdo5QCwezI4wm9J/v0X23mlZXOfBjj8Jzv3WrY5D+CsA9D7aMs2gGfjve8ArD6mePZSeCfEYt8CONWDw8FXTxrPqx/r9Vt4biXeANh8vV7/+/16ffMD1N8AuKD/A/8leAvFY9bLAAAAOGVYSWZNTQAqAAAACAABh2kABAAAAAEAAAAaAAAAAAACoAIABAAAAAEAAAAaoAMABAAAAAEAAAAWAAAAAKrxeTEAAACrSURBVEgN7VXRDoAgCKRW6/8/t/VgsglDgnTmbG31IpzdHVIqwP80dmAyeMHAWqBMO0uiWjhgaxG9cFbYEWN9DiLYzYRcpdlCoB7TSxou5l5HZovZaoJaHtddkVWAxmT1ngFxHhlJcTSVORnQaLaOJnuO3zO6axt25nsrKn3Pd1ck90epUj3vcd195BG0cG0uD1XkdDtY01/I+hyIyobcR8KPw1pjq2gWGRacsZQZJVBDLxoAAAAASUVORK5CYII=',
    'stale': 'iVBORw0KGgoAAAANSUhEUgAAABoAAAAWCAYAAADeiIy1AAAEDmlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPpu5syskzoPUpqaSDv41lLRsUtGE2uj+ZbNt3CyTbLRBkMns3Z1pJjPj/KRpKT4UQRDBqOCT4P9bwSchaqvtiy2itFCiBIMo+ND6R6HSFwnruTOzu5O4a73L3PnmnO9+595z7t4LkLgsW5beJQIsGq4t5dPis8fmxMQ6dMF90A190C0rjpUqlSYBG+PCv9rt7yDG3tf2t/f/Z+uuUEcBiN2F2Kw4yiLiZQD+FcWyXYAEQfvICddi+AnEO2ycIOISw7UAVxieD/Cyz5mRMohfRSwoqoz+xNuIB+cj9loEB3Pw2448NaitKSLLRck2q5pOI9O9g/t/tkXda8Tbg0+PszB9FN8DuPaXKnKW4YcQn1Xk3HSIry5ps8UQ/2W5aQnxIwBdu7yFcgrxPsRjVXu8HOh0qao30cArp9SZZxDfg3h1wTzKxu5E/LUxX5wKdX5SnAzmDx4A4OIqLbB69yMesE1pKojLjVdoNsfyiPi45hZmAn3uLWdpOtfQOaVmikEs7ovj8hFWpz7EV6mel0L9Xy23FMYlPYZenAx0yDB1/PX6dledmQjikjkXCxqMJS9WtfFCyH9XtSekEF+2dH+P4tzITduTygGfv58a5VCTH5PtXD7EFZiNyUDBhHnsFTBgE0SQIA9pfFtgo6cKGuhooeilaKH41eDs38Ip+f4At1Rq/sjr6NEwQqb/I/DQqsLvaFUjvAx+eWirddAJZnAj1DFJL0mSg/gcIpPkMBkhoyCSJ8lTZIxk0TpKDjXHliJzZPO50dR5ASNSnzeLvIvod0HG/mdkmOC0z8VKnzcQ2M/Yz2vKldduXjp9bleLu0ZWn7vWc+l0JGcaai10yNrUnXLP/8Jf59ewX+c3Wgz+B34Df+vbVrc16zTMVgp9um9bxEfzPU5kPqUtVWxhs6OiWTVW+gIfywB9uXi7CGcGW/zk98k/kmvJ95IfJn/j3uQ+4c5zn3Kfcd+AyF3gLnJfcl9xH3OfR2rUee80a+6vo7EK5mmXUdyfQlrYLTwoZIU9wsPCZEtP6BWGhAlhL3p2N6sTjRdduwbHsG9kq32sgBepc+xurLPW4T9URpYGJ3ym4+8zA05u44QjST8ZIoVtu3qE7fWmdn5LPdqvgcZz8Ww8BWJ8X3w0PhQ/wnCDGd+LvlHs8dRy6bLLDuKMaZ20tZrqisPJ5ONiCq8yKhYM5cCgKOu66Lsc0aYOtZdo5QCwezI4wm9J/v0X23mlZXOfBjj8Jzv3WrY5D+CsA9D7aMs2gGfjve8ArD6mePZSeCfEYt8CONWDw8FXTxrPqx/r9Vt4biXeANh8vV7/+/16ffMD1N8AuKD/A/8leAvFY9bLAAAAOGVYSWZNTQAqAAAACAABh2kABAAAAAEAAAAaAAAAAAACoAIABAAAAAEAAAAaoAMABAAAAAEAAAAWAAAAAKrxeTEAAADASURBVEgN7ZJRDsMwCEO7afe/8hYqGQVkKKB8rlKVxMHPIe11/Z/hDbyI70u0icTYyjkVIsCQFW7oMfoTZX4SrxYlNWwrvTIx7OB9zmCZtnt1nnXkYWryG2v92MWbmCIJMBnxSi30yHfrnSBA0ZmMpRAxdoP2sHLINAidoDPhPD7djgD349EgwD000k1d5/dufROTshZRkEBLJ/XAtaYHioLETw0EPJKmXbAww2KnNgWMUNQM2ywCQDW4wgoiDso/4McaHTuzczcAAAAASUVORK5CYII=',
    'acknowledged': 'iVBORw0KGgoAAAANSUhEUgAAABoAAAAWCAYAAADeiIy1AAAEDmlDQ1BrQ0dDb2xvclNwYWNlR2VuZXJpY1JHQgAAOI2NVV1oHFUUPpu5syskzoPUpqaSDv41lLRsUtGE2uj+ZbNt3CyTbLRBkMns3Z1pJjPj/KRpKT4UQRDBqOCT4P9bwSchaqvtiy2itFCiBIMo+ND6R6HSFwnruTOzu5O4a73L3PnmnO9+595z7t4LkLgsW5beJQIsGq4t5dPis8fmxMQ6dMF90A190C0rjpUqlSYBG+PCv9rt7yDG3tf2t/f/Z+uuUEcBiN2F2Kw4yiLiZQD+FcWyXYAEQfvICddi+AnEO2ycIOISw7UAVxieD/Cyz5mRMohfRSwoqoz+xNuIB+cj9loEB3Pw2448NaitKSLLRck2q5pOI9O9g/t/tkXda8Tbg0+PszB9FN8DuPaXKnKW4YcQn1Xk3HSIry5ps8UQ/2W5aQnxIwBdu7yFcgrxPsRjVXu8HOh0qao30cArp9SZZxDfg3h1wTzKxu5E/LUxX5wKdX5SnAzmDx4A4OIqLbB69yMesE1pKojLjVdoNsfyiPi45hZmAn3uLWdpOtfQOaVmikEs7ovj8hFWpz7EV6mel0L9Xy23FMYlPYZenAx0yDB1/PX6dledmQjikjkXCxqMJS9WtfFCyH9XtSekEF+2dH+P4tzITduTygGfv58a5VCTH5PtXD7EFZiNyUDBhHnsFTBgE0SQIA9pfFtgo6cKGuhooeilaKH41eDs38Ip+f4At1Rq/sjr6NEwQqb/I/DQqsLvaFUjvAx+eWirddAJZnAj1DFJL0mSg/gcIpPkMBkhoyCSJ8lTZIxk0TpKDjXHliJzZPO50dR5ASNSnzeLvIvod0HG/mdkmOC0z8VKnzcQ2M/Yz2vKldduXjp9bleLu0ZWn7vWc+l0JGcaai10yNrUnXLP/8Jf59ewX+c3Wgz+B34Df+vbVrc16zTMVgp9um9bxEfzPU5kPqUtVWxhs6OiWTVW+gIfywB9uXi7CGcGW/zk98k/kmvJ95IfJn/j3uQ+4c5zn3Kfcd+AyF3gLnJfcl9xH3OfR2rUee80a+6vo7EK5mmXUdyfQlrYLTwoZIU9wsPCZEtP6BWGhAlhL3p2N6sTjRdduwbHsG9kq32sgBepc+xurLPW4T9URpYGJ3ym4+8zA05u44QjST8ZIoVtu3qE7fWmdn5LPdqvgcZz8Ww8BWJ8X3w0PhQ/wnCDGd+LvlHs8dRy6bLLDuKMaZ20tZrqisPJ5ONiCq8yKhYM5cCgKOu66Lsc0aYOtZdo5QCwezI4wm9J/v0X23mlZXOfBjj8Jzv3WrY5D+CsA9D7aMs2gGfjve8ArD6mePZSeCfEYt8CONWDw8FXTxrPqx/r9Vt4biXeANh8vV7/+/16ffMD1N8AuKD/A/8leAvFY9bLAAAAOGVYSWZNTQAqAAAACAABh2kABAAAAAEAAAAaAAAAAAACoAIABAAAAAEAAAAaoAMABAAAAAEAAAAWAAAAAKrxeTEAAACwSURBVEgN7ZRRDoAwCEPVeP8ra5oIYabDFeef+xGB9iEal+U/xQ2sRHeQXCXFvN1nFgSGXa9uwcfQA/fcE603JT2slK4MgmgcY2aW5aLW4y1TzKzNAPnU2WBvQYA8vhMMoIDukw9DVBAmN5gEUUHoN9jQuiCwo6zONDIEwgrIgNK192ewFUlmVzN94h4IGiqokJnGvipWU3ONF5u6aVDdQ3/j3dyEphiOgke8ou838QnP1hYY/TAMVgAAAABJRU5ErkJggg=='
}
# pylint: enable=line-too-long
#state_icons = {
#    'okay': '',
#    'unknown': '',
#    'warning': '',
#    'error': '',
#    'unusable': '',
#    'stale': '',
#    'acknowledged': '',
#}

def additional_config(conf, parser):
    """ Additional configuration for xbar client.
    """
    # pylint: disable=unused-argument

    conf.add('group_by', type=str, cli=True,
        description='Group by given attribute')
    conf.add('no_group', type=str, cli=True, value='Misc',
        description='What to call group if there is none')


def local_timestamp_from_javascript(reported):
    """
    Convert Javascript-style UTC timestamp to local readable one.  For
    example:
        given "2023-06-11T16:28:26.902741Z",
        returns "2023-06-11 09:28:26 PDT"
    """
    ts_utc = datetime.strptime(reported, "%Y-%m-%dT%H:%M:%S.%f%z")
    ts_local = ts_utc.astimezone()
    return ts_local.strftime("%Y-%m-%d %H:%M:%S %Z")

def summarize_totals(totals):
    """ Summarizes totals in a short string summary.
    """
    parts = []
    nodecount = 0

    if totals.get(State.unusable, 0) > 0:
        parts.append(f"{totals[State.unusable]}U")
        nodecount += totals[State.unusable]
    if totals.get(State.error, 0) > 0:
        parts.append(f"{totals[State.error]}E")
        nodecount += totals[State.error]
    if totals.get(State.warning, 0) > 0:
        parts.append(f"{totals[State.warning]}w")
        nodecount += totals[State.warning]
    if totals.get(State.unknown, 0) > 0:
        parts.append(f"{totals[State.unknown]}u")
        nodecount += totals[State.unknown]
    if totals.get(State.okay, 0) > 0:
        nodecount += totals[State.okay]

    if totals.get('stale', 0) > 0:
        parts.append(f"{totals['stale']}s")
    if totals.get('acknowledged', 0) > 0:
        parts.append(f"{totals['acknowledged']}a")

    if parts:
        summary = ", ".join(parts) + f" of {nodecount}"
    else:
        summary = f"All {nodecount} ok"
    return summary

def _make_altline(nodename, test):
    reported = local_timestamp_from_javascript(test.reported)
    command = None
    alt_text = None
    state = State(test.state).name

    if test.acknowledged:
        acknowledged = local_timestamp_from_javascript(test.acknowledged)
        alt_text  = f"Acknowledged {acknowledged} (reported {reported})"
        # TODO: not implemented
        #command = f"unack {nodename}:{test}"
    else:
        if test.state != State.okay:
            command = f"ack -s {state} {nodename}:{test}"
            alt_text = f"Acknowledge {state} on {test} (reported {reported})"
    if not alt_text:
        alt_text = f"{test} reported {reported}"
    if command is not None:
        params = [
            f"param{i+1}={param}"
            for i, param in enumerate(command.split())
        ]
        alt_text += f" | shell={SMASH_CMD} {' '.join(params)} terminal=false refresh=true"

    alt = f"{alt_text} | alternate=true color=lightgray"
    return alt

def xbar():
    """ Interpret Smash node and status information as menus for xbar.
    """
    # load configuration
    # pylint: disable=invalid-name,broad-except
    try:
        conf = config.common(additional_config)
    except Exception as e:
        print(f"{config.APP_TAG} | color={state_colours['unknown']}")
        print("---")
        print(f"Could not load Smash configuration: {e}")
        return

    api_url = conf['server'] + '/api'
    timeout = conf['request_timeout']

    # load node and status information
    try:
        if conf.group_by:
            nodes = smash.get_nodes_by_attribute(api_url, timeout, conf.group_by, conf.no_group)
        else:
            nodes = smash.get_nodes(api_url, timeout)
    except requests.exceptions.ConnectionError:
        print(f"{config.APP_TAG} | color={state_colours['unknown']}")
        print("---")
        print("Could not connect to Smash server")
        return

    # now do the BitBar/xbar stuff
    # TODO: move this stuff to APIHandler object?
    # determine and present the overall status in menu bar
    itor = nodes.iterate()
    rootnode = next(itor)
    colour = state_colours[rootnode[2]]
    icon = state_icons[rootnode[2]]
    if rootnode[3].acknowledged:
        colour = state_colours['acknowledged']
        icon = state_icons['acknowledged']
    print(f"| color={colour} | templateImage={icon}")
    print("---")

    # create menu entries for each node and its status items
    for (nodepath, depth, state, node) in itor:

        # alternate line is for when user presses modifier while menu open
        altline = None

        # determine message, etc. based on status node type
        if isinstance(node, status.Leaf):
            # status messages may have multiple lines
            # TODO: test with statuses that have no message
            #message = '' if node.message is None else node.message.replace("\n", "; ")
            message = node.message.replace("\n", "; ")

            # create alternate line
            nodename = nodepath[-2]
            altline = _make_altline(nodename, node)

        elif isinstance(node, status.Node):
            message = summarize_totals(node.totals)
            # TODO: could use separate iterator for nodes, that knows how to
            # deal with the leaf nodes already
        else:
            message = ''

        # determine depth of menu
        prefix = (depth - 1) * "--"

        # pylint: disable=line-too-long
        if node.acknowledged:
            print(f"{prefix}{node} {message} (acknowledged) | color=lightgray | templateImage={state_icons['acknowledged']}")
        else:
            print(f"{prefix}{node} {message} | color=lightgray | templateImage={state_icons[state]}")

        if altline is not None:
            print(f"{prefix}{altline}")

    # print epilogue
    print("---")
    print(f"Smash Clients v{version.version} | href={version.homepage}")


# if this module was called directly
if __name__ == '__main__':
    xbar()
