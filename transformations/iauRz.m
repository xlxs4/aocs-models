function r = iauRz(psi, r)

s = sin(psi);
c = cos(psi);

temp1 = c*r(1,:) + s*r(2,:);
temp2 = -s*r(1,:) + c*r(2,:);

r(1,:) = temp1;
r(2,:) = temp2;