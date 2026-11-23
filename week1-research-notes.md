# Week 1 Research Notes

## Step 1 · The self-driving loop

| Step | What a human driver uses | What a self-driving car uses | What goes in → what comes out |
|---|---|---|---|
| **Sense** | Eyes (also ears and the sense of balance/motion) | Cameras, radar, lidar, ultrasonic sensors, GPS, IMU | Light, radio waves and sound from the world → raw data (images, distances, point clouds, position) |
| **Perceive** | The brain | The onboard computer running perception software (neural networks) | Raw data → meaning: objects, their size, speed and direction, lane lines, signs. The human brain receives electrical signals from the eyes and turns them into useful information; the car's computer does the same with data from its cameras, radars and lidars. |
| **Plan** | The brain: past experience, traffic rules, choosing the right reaction to a situation | Planning software on the computer: map, route, traffic rules, predictions of what other road users will do | Understood scene + goal → a decision ("steer a little left", "slow down and stop") |
| **Act** | Hands and feet | Drive-by-wire: the computer sends electronic commands to the steering motor, throttle and brakes | Decision → movement (steering angle, acceleration, braking). Motors and actuators are to the car what muscles are to a human. |

**Note on Plan:** the quality of planning depends on the software. Two cars with the same hardware can behave very differently: one with simple software, the other with a well-trained AI and well-structured code. In an emergency a human can panic or lose orientation, while a self-driving car can follow a well-thought-out procedure to minimise the damage.

### Loop diagram

![The self-driving loop: Sense → Perceive → Plan → Act](diagrams/self-driving-loop.svg)

### Questions

**1. What happens if the perceive step is wrong, for example it sees a shadow as an obstacle?**

The computer may think the shadow is a real object, for example a car. It may stop and wait for the "object" to move, or try to drive around it. Sudden braking for nothing (engineers call it *phantom braking*) is dangerous too: the car behind can crash into us. The opposite mistake is even worse: if the model thinks a real dark object is just a shadow, the car will drive into it. To avoid this, the computer-vision model must be trained to tell shadows from real objects, and other sensors (radar, lidar) can confirm whether something is really there.

**2. What happens if the whole loop is slow, for example it runs only twice a second?**

The car decides only every 0.5 seconds. At 50 km/h (about 14 m/s) it drives about 7 metres "blind" between two decisions. If a child runs onto the road during that time, the car cannot react in time, and it also cannot steer smoothly, so it swings from side to side. That is why the whole loop (sensors, computer and control) must run many times per second, usually tens of times.

**3. Which of the four steps do you think is the hardest to get right, and why?**

I think the hardest step is **perceive**, and many engineers agree. All the other steps are built on it: if the car makes a mistake here, planning and acting become useless, because they work with a wrong picture of the world. And the real world is chaotic: millions of unpredictable situations can happen on a real road (strange objects, shadows, rain, unusual behaviour of people), and we cannot list them all in advance. So although every step of a product that can endanger people's lives needs the highest attention, perception needs special attention.

---

## Step 2 · Sensors

### How lidar works

Lidar builds a 3D map of the world (a *point cloud*) using laser light. It shows objects, their size and how far away they are. If it scans continuously, it also shows which direction they are moving and how fast.

How it works: a laser sends out short pulses of light. The light reflects off surrounding objects, and part of it returns to the sensor. A detector measures the time between sending the pulse and receiving it back. Since light travels at a known speed, the distance is: **distance = (speed of light × time) / 2** (divided by 2 because the light travels there and back). The lidar measures millions of points every second, and together they form a detailed 3D map of the surroundings.

### Sensor table

| Sensor | What it measures | How it works (one sentence) | Typical range | Strong at | Fooled or blinded by | Rough price |
|---|---|---|---|---|---|---|
| **Camera** | Light: colour and brightness → images of the world | Photons hit the camera sensor (matrix), which records the colour and brightness of each pixel; many pictures per second (FPS) make a video. | Up to ~250 m (depends on the lens and camera quality) | Recognising things by look: traffic lights, signs, lane lines, people. With a powerful computer-vision system it can recognise almost everything it sees. | Rain, snow, fog, darkness, glare from the sun, a dirty lens: anything that stops light from reaching the sensor | Cheap |
| **Radar** | Distance and speed of objects | The car sends radio waves (~77 GHz, older ones 24 GHz) and the antenna receives the reflection; FMCW radar compares the frequency of sent and received waves to get distance and speed. | Up to ~250 m (car radars) | Working where cameras fail: rain, fog, darkness; measures speed directly | Interference from other radars; metal objects (bridges, manhole covers) can create false "ghost" objects; low resolution, so it cannot see shape well | Cheap–medium (~$50–200 for a car radar) |
| **Lidar** | Distance to millions of points → a 3D point cloud | Sends many laser pulses and measures the time until each one reflects from a surface and comes back. | ~200–300 m | Building a very accurate 3D map of the world, day and night | Heavy rain, fog, snow and dust scatter the laser; black or mirror-like surfaces reflect badly. (Mechanical lidars can also wear out and are sensitive to vibration.) | Expensive (hundreds to thousands of $) |
| **Ultrasonic** | Distance to nearby objects | Sends ultrasound pulses and computes the distance from the time the echo takes to come back. | ~0.2–5 m | Short distances (parking), simple and cheap design | Soft materials that absorb sound (snow, fabric), thin poles, dirt or ice on the sensor. It only gives distance: it cannot recognise objects or build a 3D map. | Cheap |
| **GPS / GNSS** | The car's position on Earth (and exact time) | Satellites with atomic clocks send radio signals with the time; the receiver measures how long each signal took from at least 4 satellites and calculates its position. More satellites = better accuracy. | Works anywhere on Earth with an open sky; accuracy ~3–5 m (a few cm with RTK correction) | Knowing where the car is on the map, anywhere in the world | Tunnels, tall buildings and anything that blocks or reflects the radio signals; jamming | Cheap (precise RTK receivers are expensive) |
| **IMU (accelerometer + gyroscope)** | The car's own acceleration and rotation | Tiny (micro) sensors have small movable parts; when the IMU moves, these parts move by inertia and the sensors detect it. | No "range": it measures the car's own motion in all 3 axes, hundreds of times per second | Measuring movement and rotation very fast; works everywhere, even in tunnels where GPS fails | Drift: small errors (bias) add up, so on its own it stays accurate only for a short time (seconds to minutes) | Cheap (high-precision ones are expensive) |

### Sensors on a real car: Waymo

![Waymo self-driving car with its sensors labelled](diagrams/waymo-sensors-labelled.webp)

*Source: Waymo, "Our Vehicle Sensors" (Waymo Safety Report, waymo.com/safety)*

<!-- TODO: for each sensor write where it is mounted and WHY it sits there. -->


