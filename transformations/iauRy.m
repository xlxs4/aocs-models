function r = iauRy(theta, r)

s = sin(theta);
c = cos(theta);

temp1 = c * r(1, :) - s * r(3, :);
temp2 = s * r(1, :) + c * r(3, :);

r(1, :) = temp1;
r(3, :) = temp2;
