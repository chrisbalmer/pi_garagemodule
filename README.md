# Pi Garage Module

A simple MQTT module to manage devices with Home Assistant using a Raspberry Pi
and an Automation HAT or PHAT.

## Work In Progress

This is just a raw copy of the code, a minimal working build. More details and
code cleanup to come as I have time to make revisions.

## Tasks

- [ ] Add birth and last will to device config publishing. I think this goes
      with availability settings on the device config.
- [ ] Use `retain=true` for publishing state updates.
- [ ] Read state from MQTT host at start/connection and update devices to match.
      This should resolve issues with a reboot of the Pi and all devices
      reverting state.