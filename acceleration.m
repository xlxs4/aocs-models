function [a] = acceleration(I, w, T)
%ACCELERATION
%   TODO: Detailed explanation goes here
a = I \ (T - cross(w, I * w));
end

