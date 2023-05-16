function [qdot] = quaternion_deriv(q,w)
%QUATERNION_DERIV Quaternion derivative
%   TODO: Detailed explanation goes here
w_quat = quaternion([0, w']);
qdot = 0.5 * q * w_quat;
end

