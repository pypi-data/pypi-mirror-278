

---

# PyLipsum

`PyLipsum` is a convenient Python library for generating Lorem Ipsum text. It provides a simple interface for retrieving random text, which is often used as placeholder in web page development and layout design. With `PyLipsum` you can easily and quickly generate text of various types and sizes, which makes this tool indispensable for developers and designers.

## Main features

- **Generation flexibility**: You can generate words, paragraphs, bytes or lists depending on your needs.
- **Custom Quantity**: Specify the number of words, paragraphs, bytes, or list items to generate.
- **Intuitive interface**: Easy to use thanks to a concise and clear API.

## Installation

You can install the library using pip:

```bash
pip install pylipsum
```

## Examples of using

```python
from pylipsum import LipsumAPI

# Create an instance of the LipsumAPI class
lipsum = LipsumAPI()

# Generate 5 words
print(lipsum.generate(5, 'words'))

# Generate 2 paragraphs
print(lipsum.generate(2, 'paragraphs'))

# Generate 50 bytes
print(lipsum.generate(50, 'bytes'))

# List generation
print(lipsum.generate(3, 'lists'))
```

`PyLipsum` makes the process of generating Lorem Ipsum text fast and easy, while providing flexibility and customization to suit your needs.

## License

This library is distributed under [Apache 2.0](LICENSE).

---

