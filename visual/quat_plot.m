function [] = quat_plot(q, w)
%QUAT_PLOT Plot the quaternion parts in time
%   TODO: Detailed explanation goes here
q = compact(q);

figure;

for i = 1:4
    subplot(2, 4, i);
    plot(q(:, i));
    title(['q', num2str(i)]);
end

for j = 1:3
    subplot(2, 4, j+4);
    plot(w(j, :));
    title(['w', num2str(j)]);
end
end
