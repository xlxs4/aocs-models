function [] = analytic_comp_plot(w0, w, I1, I3, t)
%ANALYTIC_COMP_PLOT Compare omega from results w/ analytic solutions
%   TODO: Detailed explanation goes here
wp = (1 - I3 / I1) * w0(3);
w1 = w0(1) * cos(wp * t) + w0(2) * sin(wp * t);
w2 = w0(2) * cos(wp * t) - w0(1) * sin(wp * t);
w3 = w0(3);

figure;
plot(w(1, :) - w1);
end

