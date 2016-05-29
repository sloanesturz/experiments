# CS 244 PA 3
### Reproduction Attempt of [Yin et al.](https://web.stanford.edu/class/cs244/papers/videostreaming-sigcomm2015.pdf)

# Steps to re-create our results
We recommend booting up a free-tier EC2 instance to reproduce our tests.


## Install dependencies
```bash
# 1. Clone our fork of vlc to ~/vlc
$ git clone https://github.com/sloanesturz/vlc.git
$ cd vlc && ./configure --disable-avcodec && make

# 2. Clone this repository to ~/experiments and install its dependencies
$ git clone https://github.com/sloanesturz/experiments.git

# 3. Install mahimahi
$ sudo add-apt-repository ppa:keithw/mahimahi
$ sudo apt-get update
$ sudo apt-get install mahimahi
```

## Run our baseline VLC bitrate adaptation experiments
```bash
# 1. Start the 3 webservers. You call kill them with `killall twistd`
$ ./run_servers.sh

# 2. Run the baseline experiment. This will take a long time (5+ hours)
$ python experiment.py test-results

# 3. Plot the baseline results in test-results/ directory
$ python plotter.py test-results

# 4. You can view our results by instead running
$ python plotter.py our-results

```
