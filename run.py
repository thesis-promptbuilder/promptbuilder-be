import uvicorn
from util.const_util import *

if __name__ == '__main__':
    uvicorn.run('app:blueprint', host="0.0.0.0", port=5001, reload=True)
