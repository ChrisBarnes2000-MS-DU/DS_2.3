# def f(x, n):
#   def f(x): return (x+n/x)/2
#   yield n
#   n = f(n)
  
# if __name__ == "__main__":
#   for item in f(x, 1):
#     print(item)

#   # f(x=1.0, n=5)

if __name__ == "__main__":
  x = 10
  def mathEx(x, a, b):
      """ calculate (a+b)*(x-1) """
      x=x
      x = x - 1
      c = (a+b)*x
      return c


print(mathEx(x, 1, 2))
