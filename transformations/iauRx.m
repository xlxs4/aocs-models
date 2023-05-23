function r = iauRx(phi, r)

s = sin(phi);
c = cos(phi);

temp2 = c * r(2, :) + s * r(3, :);
temp3 = -s * r(2, :) + c * r(3, :);

r(2, :) = temp2;
r(3, :) = temp3;
