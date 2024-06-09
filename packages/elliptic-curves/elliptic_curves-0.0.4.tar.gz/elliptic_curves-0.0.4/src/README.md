This package implements elliptic curves over various fields.

## Contents

The `elliptic.curves` module implements elliptic curves. An interface for fields is specified in the `elliptic.abc` module. This package provides several field implementations:
- `elliptic.mod`: modular fields
- `elliptic.fin`: Galois fields
- `elliptic.inf`: infinite fields

The implementation is not concerned with cryptographic safety. It cares for results being correct, but not secure.

## License

![GPLv3](https://www.gnu.org/graphics/gplv3-or-later.png)

This package is free software: you can redistribute it and/or modify it under the terms of the [GNU General Public License](https://www.gnu.org/licenses/) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

***

Copyright © 2023-2024 Nicolas Canceill
