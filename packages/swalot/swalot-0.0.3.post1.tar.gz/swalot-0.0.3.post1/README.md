## Installation

Install the package using pip:

```bash
pip install swalot
```

If you are using pip mirror, you may get error logs such as "No matching distribution found.."
Try using pypi as the installation source:

```bash
pip install swalot -i https://pypi.python.org/simple
```



## Usage

Simply import and wrap training code:
```python
import swalot as sw

with sw.gpu():
    """
    use CUDA tensor calculation here as usual.
    All RAM will be protected automatically!
    e.g.
    """
    # a = torch.randn(1000, 1000, 600).cuda()
    # a = torch.randn(1000, 1000, 600).to("cuda:0")
    # a = torch.randn(1000, 1000, 600, device="cuda:0")
```