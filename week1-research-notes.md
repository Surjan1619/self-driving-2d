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

**Why each sensor sits where it does**

Each sensor position has its own purpose. Waymo also makes sure that every direction around the car is covered by at least two sensors, so if one fails, another one still sees that zone.

- **Cameras and long-range lidar (roof dome):** the higher a sensor is, the farther it sees. From the roof the car can see that not only the first car ahead is stopping, but also the second and third, so it can brake even before the car in front of it does. The roof is also cleaner: there is less dirt from the road than at the bumpers. And the roof is the only place where a sensor can see all 360° around the car; anywhere else the car's own body blocks 90–180° of the view.
- **Short-range lidars (front and rear bumpers, sides near the front wheels):** placing sensors on the roof creates a new problem: in every direction there is a blind zone of about 1–3 metres right next to the car. If a child runs in front of the car, neither the roof cameras nor the roof lidar can see them. These lidars close all the blind zones. They do not see as far as the roof sensors, but they do not need to: their job is to detect everything close to the car.
- **Radars (rear corners of the roof):** each corner radar watches two sides at once: behind the car and the left or right side. This is important when changing lanes, and together the two radars make sure each zone is covered by at least two sensors.
- **GPS (roof):** the roof is the best place to receive signals from satellites, because nothing blocks the open sky.
- **IMU (inside the roof unit):** the IMU does not need to see anything; it measures the car's own movement and rotation. It sits in the same unit as the cameras and lidar, so it moves together with them, and the computer can use it to correct their data while the car is moving.
- **Microphones (supplemental sensors):** they let the car hear sirens and other sounds from any direction. With several microphones the car can also tell which side the sound is coming from.

### How Waymo drives: four questions

![How Waymo drives: localization, perception, prediction, planning](diagrams/waymo-how-it-drives.png)

[Open as PDF](diagrams/waymo-how-it-drives.pdf)

### Essay: cameras only, or cameras plus lidar and radar?

**For cameras only (Tesla).** Tesla drives with cameras only. Its argument: a human drives using only eyes and a brain, so a machine can do the same. Tesla has never used lidar in its cars and later also removed radar and ultrasonic sensors. This makes the cars cheaper and gives them fewer parts that can break. Instead, Tesla makes its software stronger, so that cameras can recognise even more than human eyes can.

**For cameras plus lidar and radar (Waymo).** Cameras alone bring more complexity. When visibility is low (fog, heavy rain, darkness, sun glare), cameras become almost useless, while radar can still help the car drive. Each sensor solves its own problem, and they depend on each other, so without one of them the car becomes less safe. For example, a camera cannot measure the distance to an object directly: the car must estimate it with a very heavy ML model, which is harder and less accurate than a lidar measuring it directly.

**My opinion.** I find the combination of cameras, lidar and radar more convincing. The sensors cover each other's weak points, and if one of them is blinded, the others still see the road. That matters more than the lower price, because a mistake can cost a life. The same idea goes beyond these three sensors: without GPS and an IMU, the car could not easily know where it is and which way it is heading.

### Which real sensor is my Week 2 car's sensor most like?

My simulated car's sensors only check whether the floor just ahead is dark (on the line) or light (off the line). They do not measure distance; they measure the brightness of one point. So they are most like a **camera with just one pixel**, or the simple infrared light sensors used on real line-following robots. Based on this information the car can follow the line and does not leave the track.

---

## Step 3 · Levels of automation (SAE J3016)

| Level | Name | Who steers and brakes? | Who must watch the road? | Who handles an emergency? | One real example |
|---|---|---|---|---|---|
| **0** | No driving automation | Human | Human | Human (the car can only warn or brake for a moment) | Lane departure warning, automatic emergency braking (AEB) |
| **1** | Driver assistance | Human + system helps with **one** task (steering **or** speed) | Human | Human | Adaptive cruise control |
| **2** | Partial driving automation | System (steering **and** speed at the same time) | Human, all the time | Human | Tesla Autopilot / FSD (Supervised) |
| **3** | Conditional driving automation | System, in limited conditions (traffic jams, highways) | System (the human may look away) | Human, when the system asks them to take over | Mercedes-Benz Drive Pilot |
| **4** | High driving automation | System, only inside its prepared zone | System | System | Waymo One robotaxi, Baidu Apollo Go, Zoox |
| **5** | Full driving automation | System, everywhere | System | System | None exists yet |

### What each level means

**Level 0 · No driving automation.** A human drives the car. The car only has features that warn the driver or help for a moment in an emergency: for example, a warning when the car is leaving its lane, or automatic emergency braking (AEB) when the car is about to crash into something in front of it. Such systems are not very hard to build, because they do not need to understand heavy traffic: they only track a few simple things.

**Level 1 · Driver assistance.** The system does only one task: for example, it keeps a safe distance from the car in front (adaptive cruise control), or it keeps the car inside the lane lines. It performs one of these tasks and no more; the human does everything else.

**Level 2 · Partial driving automation.** The car controls the steering wheel and the speed at the same time by itself, for example Tesla Autopilot / FSD (Supervised). But even though the car can drive by itself, the human must watch the road all the time and is responsible for the driving.

**Level 3 · Conditional driving automation.** The car can drive by itself in certain conditions, for example in a traffic jam or on a highway. The driver can take their hands off the steering wheel and stop watching the road, but must be ready at any moment to take the wheel when the car asks. This is one of the hardest problems in self-driving engineering. A person who has been reading or watching a film needs several seconds to understand what is happening on the road, so the car must notice a problem early and warn the driver in time. And if the driver does not respond, the car must have a plan to stop the trip safely by itself.

**Level 4 · High driving automation.** The car drives by itself without a human. Cars of this level may not even have a steering wheel. The limit is that the car can drive only inside special zones (geofenced areas) that were prepared and tested beforehand, for example Waymo One, Baidu Apollo Go or Zoox robotaxis. Inside its zone the car must handle every unexpected situation by itself, for example understand the signals of a traffic police officer. In practice this needs very accurate lidars, radars and ML models that understand the real world.

**Level 5 · Full driving automation.** A Level 5 car would have to drive everywhere a human driver can, in any weather and on any road, with no limits on where it works. Cars of this level do not exist yet.

### Five real products by SAE level

- **Ordinary adaptive cruise control: Level 1.** It controls only one task, the speed and distance to the car in front, while the driver steers.
- **Tesla Full Self-Driving (Supervised): Level 2.** It steers and controls speed at the same time, but Tesla says the driver must keep watching the road and be ready to take over at any moment; that is what "Supervised" means.
- **comma.ai openpilot: Level 2.** Like Tesla, it steers and controls speed together, but it uses a driver-facing camera to check that the driver keeps looking at the road.
- **Mercedes-Benz Drive Pilot: Level 3.** On approved highways in traffic jams, at limited speed, the driver may look away from the road (for example, watch a film on the car's screen), but must take over when the car asks.
- **Waymo robotaxis: Level 4.** There is nobody in the driver's seat at all, but the cars drive only inside the cities and zones Waymo has mapped and tested.

### Why is Level 3 the trickiest level for humans?

At Level 3 the car drives itself, so the person is allowed to stop watching the road and, for example, read a book. But when the car meets a situation it cannot handle, it asks the person to take over within a few seconds. A person who was reading needs time to look up, understand where they are, what the other cars are doing and why the car is asking for help, and those few seconds may not be enough. People also quickly start to trust the system too much and stop paying attention, which makes the handover even harder. At Level 2 the driver is always watching, and at Level 4 the car never needs the driver, so only Level 3 depends on a sudden switch from a relaxed passenger to a responsible driver.



---

## Step 5 · Failure analysis: Tesla Autopilot, Williston, Florida, May 2016

Source: NTSB, *Highway Accident Report HAR-17/02* (2017), [docs/HAR1702.pdf](docs/HAR1702.pdf)

### What happened?
On 7 May 2016 a Tesla Model S was driving east on highway US-27A in Florida. A truck coming from the other direction made a left turn across the Tesla's lanes, in front of it. The Tesla driver was not watching the road and did not notice the truck's trailer.
- **Seconds before:** the driver's last action was 1 min 51 s before the crash, when he raised the cruise speed to 74 mph. After that he did not steer or brake at all (section 1.3.5, p. 15).
- **The moment:** the car hit the side of the trailer at 74 mph (≈119 km/h); the speed limit was 65 mph (≈105 km/h). It drove under the trailer, and the trailer sheared off the car's roof (1.1.1, p. 1).
- **What happened next:** the car left the road, went through two fences, broke a utility pole and stopped about 910 feet (≈277 m) later. The Tesla driver was killed; the truck driver was not hurt (1.1.1, p. 1).

Tesla saves logs on an SD card in the car's computer and sometimes sends this data to the company. These logs are how investigators know what the car was doing (1.3.5, p. 14). The logs show that two Autopilot systems were on:
- **Traffic-Aware Cruise Control (TACC)** controls the speed. It keeps the speed the driver set and slows down, even to a full stop, if there is a car in front; then it speeds up again.
- **Autosteer** steers the car to keep it in its lane by following the lane markings.

Together these two systems make SAE Level 2 (1.3.3, p. 9). At Level 2 the driver must not stop watching the road, but the Tesla driver did. During the 41-minute trip Autopilot was on for 37 minutes, and the system felt the driver's hands on the steering wheel for only 25 seconds. It warned him 7 times to hold the wheel, and the longest time he drove without his hands on the wheel was almost 6 minutes (1.3.5, p. 14).

### Which step of the loop failed?
**Perceive.** The camera and radar were working, but the system never understood that a truck was crossing its path, so Plan and Act never reacted: no warning, no braking, no slowing down.
> "There was no record indicating that the Tesla's automation system identified the truck that was crossing in the car's path or that it recognized the impending crash." (1.3.5, p. 15)

Autopilot was not designed to recognise vehicles crossing the road (finding 3, p. 41). In 2016 no car company's emergency braking was designed for crossing traffic (2.2.4, p. 30). The human's own loop also failed: the driver was not looking, so he never sensed the truck.

### What did the humans and the company get wrong?
- **The truck driver** had to yield the right of way and did not (2.2.2, p. 30).
- **The Tesla driver.** At Level 2 the driver must (2.5, p. 34):
  - monitor the automation;
  - understand what is happening on the road;
  - know the system's limits;
  - be ready to take control at any moment.

  He did none of this: he trusted the automation too much (findings 7–8, p. 41).
- **Tesla:**
  - Autopilot could be switched on on roads it was not designed for. The manual said "highways and limited-access roads only", but the car did not block other roads (2.4, p. 33).
  - Many cars check that the driver's hands are on the wheel by measuring the turning force (torque) on it. But driving is mainly about the eyes: a driver can hold the wheel without looking at the road (finding 6, p. 41). Some newer systems, such as Cadillac Super Cruise, use a camera to track the driver's head or eyes (2.5, p. 35).

NTSB's probable cause: the truck driver did not yield, and the Tesla driver was inattentive because he relied too much on the automation and did not react. Autopilot's design made this worse, because it let him stop paying attention for a long time and use it in ways Tesla's own manual warned against (3.2, p. 42).

### What changed afterwards?
On 23 September 2016 Tesla sent firmware version 8 to all its cars. It changed the driver interface and the warning logic (1.3.6, p. 16):
- The driver can now keep his hands off the wheel for less time before the car warns him.
- After 3 warnings, Autosteer switches off and cannot be used for one hour or until the car is restarted.
- On preferred roads there are no warnings below 8 mph. The first warning comes after 10 minutes at 8–45 mph, and after 2–3 minutes above 45 mph.

But even after this update Autopilot can still be used on any road with clear lane markings (2.4, p. 33). The NTSB asked car makers to allow automation only where it was designed to work (H-17-41) and to find better ways to check that the driver is paying attention (H-17-42) (4.1, p. 43).

### My recommendation
A camera on the steering column tracks the driver's eyes instead of checking for hands on the wheel, because a driver can hold the wheel without looking at the road (finding 6, p. 41).
1. If the driver's eyes are off the road for more than 15 seconds, the car sounds an alarm.
2. After 3 alarms in a row with no response, the car slows down, moves to the right side of the road and stops with the hazard lights on. Today's systems stop in the travel lane; NTSB expects future systems to leave the lane before stopping (2.5, footnote 63, p. 34).
3. If the driver still does not respond after the car has stopped, for example because he is asleep or feels ill, the car calls 911.

This fixes the **Sense and Perceive** steps of the loop *for the driver*: the car can finally tell whether the human is watching the road. The final stop is the **Act** step.

**How to test it:** a test driver looks away from the road on a closed test track. The alarm must sound within 5 seconds, and after 3 ignored alarms the car must stop on the right side of the road.

### Link to my project
My Week 2 car can make the same kind of mistake. Its sensors only report "on the dark line" or "not on the line". If all of them see nothing, `brain()` returns 0, so the car drives straight ahead and leaves the track without "knowing" that anything is wrong. Like the Tesla, it treats "I see nothing" as "nothing is there".

"Sees nothing" can mean two things: the car has drifted off the line, or the sensors are broken or blocked. The car cannot tell which, so it should do this:
1. Slow down and keep steering towards the side where it last saw the line.
2. If the line appears again within 1 second (60 frames), it carries on driving normally.
3. If the line does not appear, it stops, because it must assume its sensors are broken or blocked.

This fixes the **Plan** step: the car decides that "no data" means danger. I will build this in Step 10, challenge B.

---

## Step 6 · Reading the starter code

**1. Which functions do SENSE, THINK and ACT?**
SENSE is `read_sensors(car, track)`, and ACT is `car.move(steer)` (main.py, lines 112–114). The THINK line uses two functions: if autopilot is on, `brain(readings)` decides how to steer from the sensor readings; if it is off, `keyboard_steer()` reads the arrow keys and the human drives.

**2. How many times per second does the loop run?**
60 times. `FPS = 60` (line 15), and `clock.tick(FPS)` (line 128) waits at the end of every loop so it never runs faster than 60 frames per second.

**3. What does `on_line()` check?**
It checks whether a point is inside the window and whether the pixel of the track under it is dark. It adds up the red, green and blue values: the line `(40, 40, 40)` gives 120 and the floor `(235, 235, 225)` gives 695. Anything below 300 counts as "on the line".

**4. Why is the track drawn on its own surface `track`?**
The sensors read colours from `track`, which only has the floor and the line. If they read from `screen`, they would also see the red car and the blue sensor dots drawn on top. For example, a sensor under the car would read red, and red is not dark, so it would wrongly say "not on the line".

---

## Step 7 · Experiments

**1. Speed.** 3 laps by hand:

| Speed | Frames off line | Frames for 3 laps (approx.) | Share of time off the line |
|---|---|---|---|
| 2 | 141 | ≈ 2640 | ≈ 5 % |
| 4 | ≈ 800 | ≈ 1320 | ≈ 60 % |

The oval is about 1760 pixels long, so 3 laps take about 2640 frames at speed 2 but only about 1320 frames at speed 4. Even though the faster laps are twice as short in time, the car was off the line almost 6 times more often. At speed 4 the car moves twice as far each frame, so I have less time to react, and in the curves I could not turn fast enough to stay on the line.

**2. TURN_RATE.**
- At 1.0 the car turns only 1 degree per frame, so it turns very slowly. Even with the arrow held down it can barely get round the ends of the oval and drifts outwards. At speed 2 its tightest circle has a radius of about 115 pixels, about the same as the curves at the ends of the oval, so there is no margin.
- At 10.0 the car turns 10 degrees per frame. A short tap already jerks it to the side, so it is hard to drive straight; holding the key spins it almost on the spot.
- 4.0 is a good middle: fast enough for the curves, but still controllable.

**3. Why is −1 / 0 / +1 steering not smooth?**
Sometimes the car needs to turn just a little and sometimes a lot, but the keyboard only gives "straight" or "full turn". The oval is a long gentle curve that needs a small steer such as +0.3. With the keyboard I have to keep pressing and releasing the key: released, the car drifts off the outside of the line; pressed, it turns too hard to the inside. So it zig-zags instead of following a smooth arc. If my `brain()` in Step 9 only returns −1, 0 or +1, the autopilot will wobble in the same way.

---

## Step 8 · Sensors

Two sensors, 25 pixels ahead of the car, 30° to the left and 30° to the right of its heading. Each one says `True` if it is on the dark line.

| Situation | Left sensor | Right sensor |
|---|---|---|
| Car centred on the line, going straight | True | True |
| Car drifting so the line is to its left | True | False |
| Car drifting so the line is to its right | False | True |
| Car completely off the line | False | False |

**Which situations can my car not tell apart?** When the car is completely off the line, both sensors read `False`, whether the car has left the oval on the inside or on the outside. So the car does not know which side the line is on, and it does not know which way to steer back. The two sensors also do not tell the car at what angle it is crossing the line. (Same problem as in Step 5: "I see nothing" does not say where the danger is. Fix: remember on which side the line was seen last.)

### Experiment: sensor distance and angle
I slid the car sideways across the top straight of the oval (the line is 30 px wide) and noted where the readings change.

| Setting | Reading when centred | Both `True` while the car is within | Result |
|---|---|---|---|
| distance 25, angles ±30 (default) | True, True | ±2 px of the centre | Reacts as soon as the car drifts; good |
| distance 10, angles ±30 | True, True | ±10 px | **Too late** |
| distance 60, angles ±30 | **False, False** | never | **Wrong**: says "off the line" when it is on it |
| distance 25, angles ±10 | True, True | ±9 px | **Too late** |
| distance 25, angles ±60 | **False, False** | never | **Wrong**, like distance 60 |

- **Too close (distance 10 or angles ±10):** the two sensors are almost in the same place, so both stay `True` until the car is already near the edge of the line. The autopilot will only react when it is about to leave the line, so it will bounce from one edge to the other instead of driving in the centre. Being so close to the nose also means it sees the curve late, and at higher speed it will not manage to turn in time.
- **Too far (distance 60 or angles ±60):** the sensors end up further apart than the line is wide, so when the car is perfectly centred both sensors are on the light floor and read `False`. The car "thinks" it has left the road when it has not. Far-ahead sensors can also touch the line before the car reaches it, for example when the car comes back towards the line at an angle, so they make it turn too early and miss the line.
- **The best setting is in the middle:** the two sensors must sit just inside the edges of the line, so that a small drift changes one reading straight away.
