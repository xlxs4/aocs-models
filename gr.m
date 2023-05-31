p = [6878000 6878000 6878000];
h = 1e-3;
G = zeros(3);
for i = 1:3
    e = zeros(1, 3);
    e(i) = 1;
    [gxp, gyp, gzp] = gravitysphericalharmonic(p + h*e);
    [gxm, gym, gzm] = gravitysphericalharmonic(p - h*e);
    gp = [gxp; gyp; gzp];
    gm = [gxm; gym; gzm];
    dgdr = (gp-gm)/(2*h);
    G(:,i) = dgdr;
end
