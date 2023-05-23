function [] = quat_animate(q, dt)
%QUAT_ANIMATE Animate the object in S4
%   TODO: Detailed explanation goes here
tp = theaterPlot('XLimit', [-2, 2], 'YLimit', [-2, 2], 'ZLimit', [-2, 2]);
op = orientationPlotter(tp, 'DisplayName', 'Orientation', ...
    'LocalAxesLength', 2);

for i = 1:numel(q)
    plotOrientation(op, q(i));
    pause(dt/100); % assume dt < 1
end
end
