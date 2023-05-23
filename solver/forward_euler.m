function [q, w] = forward_euler(torque, h, I, q0, w0)
%FORWARD_EULER Forward Euler method
%   TODO: Detailed explanation goes here
q = q0 + h * quaternion_deriv(q0, w0);
q = normalize(q);

w = w0 + h * acceleration(I, w0, torque(q0, w0));
end
