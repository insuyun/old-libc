# old-libc: a tool to compile with old glibc

This is a tool to compile with old glibc. I made this for testing exploit techniques for multiple glibc versions

## Setup
```
$ apt install python2 python2-pip python3 python3-pip
$ pip2 install -r requirements-python2.txt
```

## Usage
```
$ ./old-libc.py <your-gcc-args>
```

## Example
```
$ ./old-libc.py -o test.out test.c
```

## Reference
- https://github.com/matrix1001/glibc-all-in-one
- https://github.com/shellphish/how2heap