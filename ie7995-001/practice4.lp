\ENCODING=ISO-8859-1
\Problem name: 

Minimize
 obj: 150 x1 + 230 x2 + 260 x3
  - 56.6610 w11 + 79.3254 y11 - 50 w21 + 70 y21 - 12 w31 - 3.3333 w41
  - 56.6610 w12 + 79.3254 y12 - 50 w22 + 70 y22 - 12 w32 - 3.3333 w42 
  - 56.6610 w13 + 79.3254 y13 - 50 w23 + 70 y23 - 12 w33 - 3.3333 w43 
Subject To
 c1: x1 + x2 + x3 <= 500
 c2: 3.0 x1 + y11 - w11 >= 200
 c3: 3.6 x2 + y21 - w21 >= 240
 c4: 24 x3 - w31 - w41 >= 0
 c5: w31 <= 6000
 c6: 2.5 x1 + y12 - w12 >= 200
 c7: 3.0 x2 + y22 - w22 >= 240
 c8: 20 x3 - w32 - w42 >= 0
 c9: w32 <= 6000
 c10: 2.0 x1 + y13 - w13 >= 200
 c11: 2.4 x2 + y23 - w23 >= 240
 c12: 16 x3 - w33 - w43 >= 0
 c13: w33 <= 6000
End