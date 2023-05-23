function [q, w] = runge_kutta4(torque, h, I, q0, w0)
%RUNGE_KUTTA4 4th order Runge-Kutta method
%   TODO: Detailed explanation goes here
dw1 = h * acceleration(I, w0, torque(q0, w0));
dq1 = h * quaternion_deriv(q0, w0);

dw2 = h * acceleration(I, w0+dw1/2, torque(q0+dq1./2, w0+dw1/2));
dq2 = h * quaternion_deriv(q0+dq1./2, w0+dw1/2);

dw3 = h * acceleration(I, w0+dw2/2, torque(q0+dq2./2, w0+dw2/2));
dq3 = h * quaternion_deriv(q0+dq2./2, w0+dw2/2);

dw4 = h * acceleration(I, w0+dw3, torque(q0+dq3./2, w0+dw3/2));
dq4 = h * quaternion_deriv(q0+dq3, w0+dw3);

q = q0 + 1 / 6 * (dq1 + 2 * dq2 + 2 * dq3 + dq4);
q = normalize(q);

w = w0 + 1 / 6 * (dw1 + 2 * dw2 + 2 * dw3 + dw4);
end
