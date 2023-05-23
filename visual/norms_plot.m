function [] = norms_plot(w)
%NORMS_PLOT Plot the norm of omega in time
%   TODO: Detailed explanation goes here
norms = sqrt(sum(w.^2,1));
figure;
plot(norms);
end

