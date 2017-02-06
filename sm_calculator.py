#!/usr/bin/env python3
"""Feb 4 2017 Calculator Exercise."""

index_page = """<html>
 <body>
   <h1>Home Page</h1>
   <p>Click on link to see the result</p>
   <p><a href="/add/10/20">add</a> 10 and 20</p>
   <p><a href="/subtract/20/10">subtract</a> 10 from 20</p>
   <p><a href="/subtract/10/20">subtract</a> 20 from 10</p>
   <p><a href="/subtract/10/-20">subtract</a> -20 from 10</p>
   <p><a href="/multiply/20/10">multiply</a> 20 and 10</p>
   <p><a href="/multiply/20/0">multiply</a> 20 and 0</p>
   <p><a href="/divide/20/10">divide</a> 20 by 10</p>
   <p><a href="/divide/20/0">division by zero</a> 20 by 0</p>
   <p>To test: http://localhost:8085/operand/number1/number2</p>
   <p>operand = add or subtract or multiply or divide.</p>
 </body>
</html>
"""

def application(environ, start_response):
    """Application to return arithmetic operation on two numbers"""
    headers = [('content-type', 'text/html')]
    if environ['PATH_INFO'] == '/':
        start_response('200 OK', headers)
        return [index_page.encode()]
    else:
        try:
            path = environ.get('PATH_INFO', None)
            if path is None:
                raise Nameerror
            func, nums = resolve_path(path)
            body = func(*nums)
            status = "200 OK"
        except NameError:
            status = "404 Not Found"
            body = "<h1>Not Found </h1>"
        except ZeroDivisionError:
            status = "200 OK"
            body = "<h1> Cannot Divide by zero </h1>"
        except Exception:
            print("Exception:", Exception)
            status = "500 Internal Server Error"
            body = "<h1>Internal Server Error</h1>"
        finally:
            headers.append(('Content-length', str(len(body))))
            start_response(status, headers)
            return [body.encode('utf8')]


def resolve_path(path):
    nums = path.strip("/").split("/")
    func_name = nums.pop(0)
    func = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
    }.get(func_name)
    return func, nums


def add(*nums):
    sum = int(nums[0]) + int(nums[1])
    # print("Number1 + Number2 = ", sum)
    return str(sum)


def subtract(*nums):
    sub = int(nums[0]) - int(nums[1])
    # print("Number1 - Number2 = ", sub)
    return str(sub)


def multiply(*nums):
    mul = int(nums[0]) * int(nums[1])
    # print("Number1 * Number2 = ", mul)
    return str(mul)


def divide(*nums):
    div = int(nums[0]) / int(nums[1])
    # print("Number1 / Number2 = ", div)
    return str(div)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8085, application)
    srv.serve_forever()