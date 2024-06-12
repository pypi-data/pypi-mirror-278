# Library Name: fb2reader
## Description
fb2reader is a Python library designed for extracting data from FB2 format files. With this library, you can easily extract information about authors, titles, descriptions, covers, and the content of books in FB2 format. The library uses BeautifulSoup for XML parsing and provides convenient methods for working with the data.
## Features
Extract book identifier.
Extract book title.
Extract book body and save it as an HTML file.
Extract author information (first name and last name).
Extract book series.
Extract book language.
Extract book description.
Extract book genres.
Extract translator information.
Extract ISBN.
Extract and save book cover.

## Installation
You can install the library using pip:

``` cmd
pip install fb2reader
```

## Usage Example

``` python

import fb2reader 
file_path = 'test.fb2'
book = fb2reader.fb2(file_path)

print(book.get_isbn())
print(book.get_title())
```

### Requirements
Python 3.2+
BeautifulSoup4
