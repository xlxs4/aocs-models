iter = 10000;
dt = 0.01;

q0 = quaternion(1, 0, 0, 0);
w0 = [1; 0.7; -0.3];

q = quaternion(zeros(iter, 4))';
w = zeros(3, iter);

q(:, 1) = q0;
w(:, 1) = w0;

I1 = 1;
I2 = 1;
I3 = 0.5;

I = diag([I1, I2, I3]);

for i = 2:iter
    [qnext, wnext] = runge_kutta4(@torque, dt, I, q(:, i-1), w(:, i-1));
    q(:, i) = qnext;
    w(:, i) = wnext;
end

% quat_animate(q, dt);
% quat_plot(q,w);
% norms_plot(w);
% t = 0:dt:(iter-1)*dt;
% analytic_comp_plot(w0, w, I1, I3, t);