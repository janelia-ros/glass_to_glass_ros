- [About](#org21a16ff)
- [Usage](#orga030137)
- [Messages](#orgdd60e59)
- [Topics](#orgf035709)
- [Service Files](#orgac5f237)
- [Services](#org2fc16ad)
- [Setup](#orgf41916a)
- [Development](#orgcef185d)

    <!-- This file is generated automatically from metadata -->
    <!-- File edits may be overwritten! -->


<a id="org21a16ff"></a>

# About

```markdown
- ROS Package Names:
  - weigher
  - weigher_interfaces
- ROS Distribution: humble
- Description: This repository contains ROS 2 packages that publish weight messages from a digital scale.
- Version: 1.0.0
- Weigher Package: weigher
- Weigher Node Name: weigher
- Weigher Launch File: weigher_launch.py
- Weigher Messages:
  - Weight.msg
  - WeightArray.msg
- Weigher Topics:
  - /weigher/weight
  - /weigher/weight_thresholded
  - /weigher/weight_array
  - /weigher/weight_array_thresholded
- Weigher Service Files:
  - Tare.srv
- Weigher Services:
  - /weigher/tare
- Docker Image Name: weigher:humble
- Release Date: 2023-02-16
- Creation Date: 2022-12-14
- License: BSD-3-Clause
- URL: https://github.com/RatCity-Habitat/weigher_ros
- Author: Peter Polidoro
- Email: peter@polidoro.io
- Copyright: 2023 Howard Hughes Medical Institute
- References:
  - https://github.com/janelia-pypi/loadstar_sensors_interface_python
- Python Dependency List: loadstar_sensors_interface
```


<a id="orga030137"></a>

# Usage


## Publisher

-   Connect weigh scale to Raspberry Pi USB port.
-   Connect Raspberry Pi to power and Ethernet.

Scale will be tared on power up and automatically begin publishing weight messages.


## Subscriber

On a computer connected to the same network as the Raspberry Pi, either use Docker or install ROS 2 to subscribe to weight messages.


### Docker

```sh
docker run -it --net=host --pid=host weigher:humble ros2 topic list
docker run -it --net=host --pid=host weigher:humble ros2 topic echo /weigher/weight
docker run -it --net=host --pid=host weigher:humble ros2 topic echo /weigher/weight_thresholded
docker run -it --net=host --pid=host weigher:humble ros2 topic echo /weigher/weight_array
docker run -it --net=host --pid=host weigher:humble ros2 topic echo /weigher/weight_array_thresholded
```


### ROS 2 on Ubuntu

```sh
source ~/ros2_ws/install/setup.bash
ros2 topic list
ros2 topic echo /weigher/weight
ros2 topic echo /weigher/weight_thresholded
ros2 topic echo /weigher/weight_array
ros2 topic echo /weigher/weight_array_thresholded
```


## Services

On a computer connected to the same network as the Raspberry Pi, either use Docker or install ROS 2 to use weigher services.


### Docker

```sh
docker run -it --net=host --pid=host weigher:humble ros2 service list
docker run -it --net=host --pid=host weigher:humble ros2 service call /weigher/tare weigher_interfaces/srv/Tare
```


### ROS 2 on Ubuntu

```sh
source ~/ros2_ws/install/setup.bash
ros2 service list
ros2 service call /weigher/tare weigher_interfaces/srv/Tare
```


## Connect to Raspberry Pi for development and monitoring


### SSH into Raspberry Pi

```sh
ssh weigher@weigher.local
```


### Web Console

<https://weigher.lan:9090/>

-   username: weigher
-   password:


<a id="orgdd60e59"></a>

# Messages


## Weight.msg

```text
# This file is generated automatically from metadata
# File edits may be overwritten!

# Single weight reading.
builtin_interfaces/Time stamp
float64 weight # Measurement of the Weight in grams.
```


## WeightArray.msg

```text
# This file is generated automatically from metadata
# File edits may be overwritten!

# Multiple weight readings.
Weight[] array
```


<a id="orgf035709"></a>

# Topics


## weight

Send all messages from the digital scale one at a time along with a timestamp for that measurement.

```text
$ ros2 topic echo /weigher/weight
---
stamp:
  sec: 1676470173
  nanosec: 765260627
weight: 0.13607771100000002
---
stamp:
  sec: 1676470173
  nanosec: 883177140
weight: 0.0
---
stamp:
  sec: 1676470174
  nanosec: 11527425
weight: 0.04535923700000001
---
stamp:
  sec: 1676470174
  nanosec: 176475007
weight: 0.18143694800000004
---
```

```text
$ ros2 topic hz /weigher/weight
average rate: 574.719
        min: 0.000s max: 0.038s std dev: 0.00568s window: 2338
average rate: 576.536
        min: 0.000s max: 0.038s std dev: 0.00566s window: 2922
```


## weight\_thresholded

Send some messages from the digital scale one at a time along with a timestamp for that measurement, if the weight value exceeds a threshold. The threshold value is set with the threshold parameter.

```text
$ ros2 topic echo /weigher/weight_thresholded
---
stamp:
  sec: 1676470255
  nanosec: 932870887
weight: 520.8601184710001
---
stamp:
  sec: 1676470256
  nanosec: 19947998
weight: 504.39471544000014
---
stamp:
  sec: 1676470256
  nanosec: 161346684
weight: 499.8134325030001
---
stamp:
  sec: 1676470256
  nanosec: 301352968
weight: 498.5887331040001
---
```

```text
$ ros2 topic hz /weigher/weight_thresholded
average rate: 503.230
        min: 0.000s max: 0.054s std dev: 0.00695s window: 5102
average rate: 503.906
        min: 0.000s max: 0.054s std dev: 0.00697s window: 5613
```


## weight\_array

Send an array of Weight messages to increase the size and decrease the frequency of messages published on this topic. The maximum array length is set by the weight\_array\_length\_max parameter.

```text
$ ros2 topic echo /weigher/weight_array
---
array:
- stamp:
    sec: 1676473446
    nanosec: 920160731
  weight: 2.0411656650000003
- stamp:
    sec: 1676473446
    nanosec: 921633371
  weight: 2.0411656650000003
- stamp:
    sec: 1676473446
    nanosec: 922349652
  weight: 2.0865249020000003
- stamp:
    sec: 1676473446
    nanosec: 922925743
  weight: 2.0865249020000003
- '...'
---
```

```text
$ ros2 topic hz /weigher/weight_array
average rate: 0.287
        min: 3.460s max: 3.495s std dev: 0.01312s window: 4
average rate: 0.288
        min: 3.454s max: 3.495s std dev: 0.01571s window: 5
```


## weight\_array\_thresholded

Send an array of Weight messages to increase the size and decrease the frequency of messages published on this topic. The maximum array length is set by the weight\_array\_length\_max parameter.

Only include weight messages in the array if the weight value exceeds a threshold. The threshold value is set with the threshold parameter.

Do not send empty arrays.

```text
$ ros2 topic echo /weigher/weight_array_thresholded
---
array:
- stamp:
    sec: 1676473988
    nanosec: 201336549
  weight: 491.467332895
- stamp:
    sec: 1676473988
    nanosec: 202358047
  weight: 491.467332895
- stamp:
    sec: 1676473988
    nanosec: 203483274
  weight: 491.467332895
- stamp:
    sec: 1676473988
    nanosec: 204520182
  weight: 491.467332895
- '...'
---
```

```text
$ ros2 topic hz /weigher/weight_array_thresholded
average rate: 0.251
        min: 3.933s max: 4.048s std dev: 0.04806s window: 4
average rate: 0.251
        min: 3.933s max: 4.048s std dev: 0.04406s window: 5
```


<a id="orgac5f237"></a>

# Service Files


## Tare.srv

```text
# This file is generated automatically from metadata
# File edits may be overwritten!

---
builtin_interfaces/Time stamp
bool success
```


<a id="org2fc16ad"></a>

# Services


## tare

```text
$ ros2 service call /weigher/tare weigher_interfaces/srv/Tare
requester: making request: weigher_interfaces.srv.Tare_Request()

response:
weigher_interfaces.srv.Tare_Response(stamp=builtin_interfaces.msg.Time(sec=1676492636, nanosec=617772030), success=True)
```


<a id="orgf41916a"></a>

# Setup


## Subscriber


### Docker

1.  Install Docker

    <https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository>

2.  Clone this repository

    ```sh
    git clone https://github.com/RatCity-Habitat/weigher_ros.git
    ```

3.  Make Docker image

    ```sh
    cd weigher_ros
    docker build -f .metadata/docker/Dockerfile -t weigher:humble .
    # or
    make -f .metadata/Makefile docker-image
    ```


### ROS 2 on Ubuntu

1.  Install ROS 2

    ```text
    https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
    ```

2.  Create ROS 2 Workspace and clone this repository

    ```sh
    mkdir -p ~/ros2_ws/src && \
    cd ~/ros2_ws/src && \
    git clone https://github.com/RatCity-Habitat/weigher_ros.git
    ```

3.  Setup Python virtualenv

    ```sh
    sudo apt install python3-venv
    cd ~/ros2_ws
    make -f src/weigher_ros/.metadata/Makefile virtualenv
    ```

4.  Build ROS packages

    1.  Source the ROS underlay and activate the Python virtualenv and build ROS packages
    
        ```sh
        # build may finish with stderr warnings about deprecated setup.py install
        # if using Python 3.10 or higher
        cd ~/ros2_ws && \
        make -f src/weigher_ros/.metadata/Makefile ros-build
        ```


## Publisher


### Raspberry Pi

1.  Setup Raspberry Pi

    <https://github.com/janelia-experimental-technology/raspberrypi_setup>
    
    -   username: weigher
    -   hostname: weigher

2.  SSH into Raspberry Pi

    ```sh
    ssh weigher@weigher.local
    ```

3.  Web Console

    <https://weigher.lan:9090/>

4.  Clone Repository

    ```sh
    cd ~ && \
    git clone git@github.com:RatCity-Habitat/weigher_ros.git
    ```

5.  Add deploy ssh key to Github Repository

    ```sh
    cat .ssh/id_ed25519.pub
    ```

6.  Install make for metadata commands

    ```sh
    sudo apt install make
    ```

7.  Docker image

    ```sh
    cd ~/weigher_ros && \
    make -f .metadata/Makefile docker-image
    ```

8.  Pi Setup

    ```sh
    cd ~/weigher_ros && \
    make -f .metadata/Makefile pi-setup
    sudo reboot
    ```

9.  Check docker and systemd service

    ```sh
    systemctl status docker
    systemctl status weigher-attached@00.service
    systemd-analyze plot > boot_analysis.svg
    docker container list
    ```


<a id="orgcef185d"></a>

# Development


## Docker


### Run Docker container

```sh
make -f .metadata/Makefile docker-container
```


### Run Docker container with serial port access

```sh
make -f .metadata/Makefile docker-container-port
```


### Run Docker container and start publishing weight messages

```sh
make -f .metadata/Makefile docker-publish-weight
```


### Run Docker container and echo weight messages

```sh
make -f .metadata/Makefile docker-echo-weight-array
make -f .metadata/Makefile docker-echo-weight-array-thresholded
```


### Run Docker container and tare scale

```sh
make -f .metadata/Makefile docker-tare
```


### Stop all Docker containers

```sh
docker stop $(docker ps -aq)
```


### Find running container Name

```sh
docker ps
```


### Run bash commands in running container

```sh
docker exec -it container-name bash
```


## Ubuntu


### Build

1.  Source the ROS underlay and activate the Python virtualenv and build ROS packages

    ```sh
    # build may finish with stderr warnings about deprecated setup.py install
    # if using Python 3.10 or higher
    cd ~/ros2_ws && \
    make -f src/weigher_ros/.metadata/Makefile ros-build
    ```


### Run

1.  Source the ROS underlay and overlay and activate Python virtualenv and run the weigher node

    1.  Launch file
    
        ```sh
        source ~/ros2_ws/src/weigher_ros/.metadata/setup.bash && \
        source ~/ros2_ws/install/setup.bash && \
        ros2 launch weigher weigher_launch.py
        ```
    
    2.  ROS Run
    
        ```sh
        source ~/ros2_ws/src/weigher_ros/.metadata/setup.bash && \
        source ~/ros2_ws/install/setup.bash && \
        ros2 run weigher weigher
        ```

2.  Echo the weigher topics

    ```sh
    # Open a new termial
    source ~/ros2_ws/install/setup.bash
    ros2 topic echo /weigher/weight
    ros2 topic echo /weigher/weight_thresholded
    ros2 topic echo /weigher/weight_array
    ros2 topic echo /weigher/weight_array_thresholded
    ```


## Raspberry Pi


### Update

```sh
cd ~/weigher_ros
git pull
make -f .metadata/Makefile docker-image
make -f .metadata/Makefile pi-setup
sudo reboot
```


## Metadata


### Install Guix

[Install Guix](https://guix.gnu.org/manual/en/html_node/Binary-Installation.html)


### Clone Repository

```sh
git clone git@github.com:RatCity-Habitat/weigher_ros.git
```


### Edit metadata.org

```sh
make -f .metadata/Makefile metadata-edits
```


### Tangle metadata.org

```sh
make -f .metadata/Makefile metadata
```