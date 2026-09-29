# telemetry-geotag

Turn ordinary drone video into geotagged still imagery that a photogrammetry pipeline can
consume.

## The problem

Photogrammetry tooling — OpenDroneMap, Pix4D, Agisoft — expects a set of still photographs with
GPS position and camera parameters written into each image's EXIF metadata. The standard way to
produce that is a programmed grid mission: the aircraft flies a lawnmower pattern at fixed
altitude and triggers the shutter at a set interval, and every resulting photo is geotagged by
the aircraft as it is written.

Search and rescue drone flights do not look like that. During a live search the pilot is flying
reactively, following terrain and drainages, orbiting anything that looks like a clue, and
recording continuous video rather than stills. That is the correct way to fly a search. It also
means the imagery is, from a mapping standpoint, unusable: the sensor captured the ground in
detail, but the frames carry no position information, so nothing downstream can place them.

The data to fix this already exists. The aircraft writes a flight log alongside the video, and
that log contains position, altitude, and attitude sampled throughout the flight. The video
frames and the telemetry samples are two recordings of the same flight on a shared clock. This
tool joins them.

## What this produces

A directory of JPEGs with EXIF GPS and camera metadata written in, suitable for handing directly
to WebODM or any other photogrammetry pipeline.

Downstream of that, the output has been used to generate ~5 cm/pixel orthophotos of search areas
— roughly an order of magnitude finer than the aerial basemap imagery available for the same
ground — which can then be reprojected and loaded into mapping software as a custom layer.

The practical consequence is that an archive of past mission footage becomes a source of
high-resolution imagery after the fact, without reflying anything.

## How it works

1. **Frame extraction.** `ffmpeg` samples the video at a fixed rate. See `commands.txt` for the
   invocation currently in use.
2. **Timestamp reconstruction.** Each extracted frame is assigned a capture time derived from the
   video's start time and the frame's position in the sequence.
3. **Telemetry join.** Each frame timestamp is matched against the flight log and the aircraft
   state at that instant is resolved.
4. **EXIF write.** Position, altitude, and camera parameters are written into each frame's EXIF
   headers.
5. **Photogrammetry.** The geotagged frames are fed to WebODM for orthophoto generation.

> **TODO:** describe the telemetry format the parser expects (DJI flight record, Airdata CSV
> export, SRT subtitle track?), how the time base is established, and whether interpolation
> between telemetry samples is performed or the nearest sample is taken.

## Requirements

- Python (see `requirements.txt`)
- `ffmpeg` on `PATH`
- A flight log covering the same period as the video

## Usage

> **TODO:** entry point, arguments, and the variables in `.env.sample`.

```
cp .env.sample .env
# edit .env
python -m src.<entrypoint> --video <path> --telemetry <path> --out <dir>
```

## Accuracy and limitations

This is a recovery technique, not a replacement for flying a proper mapping mission. A programmed
grid flight produces materially better reconstructions, and if the imagery matters and the area
can be reflown, it should be.

Known sources of error:

- **Time alignment.** Geotag accuracy is bounded by how well the video clock and the telemetry
  clock agree. Any constant offset between them displaces every frame in the same direction,
  which is easy to miss because the output still looks internally consistent.
- **Overlap is not guaranteed.** Photogrammetry wants dense, regular overlap between adjacent
  images. A reactive search flight provides whatever overlap it happens to provide — heavy where
  the pilot orbited, absent where the aircraft transited quickly. Reconstruction quality varies
  across a single flight for this reason.
- **Motion blur.** Frames are sampled on a fixed interval with no regard for aircraft speed or
  sharpness, so some proportion are too blurred to contribute useful features.
- **Oblique and varying camera angles.** Grid missions hold the gimbal nadir. Search flights do
  not, and off-nadir frames are harder to reconstruct from and can distort the result.
- **Rolling shutter.** Most consumer drone cameras use a rolling shutter, which introduces
  geometric distortion proportional to motion during frame readout.

Results in practice: usable orthophotos are achievable from reactive search footage, but the
success rate is lower and the output is less clean than from a planned grid mission.

## Known future work

- **Sharpness-aware frame selection.** Score candidate frames (variance of Laplacian or similar)
  and keep the sharpest frame within each window rather than taking every nth frame blindly. This
  is the highest-value improvement — it directly attacks the motion blur problem and reduces the
  input set at the same time.
- **Adaptive sampling rate.** Derive the extraction interval from ground speed and altitude in
  the telemetry so that sampling targets a desired forward overlap percentage, rather than a
  fixed 1 fps that oversamples hovers and undersamples fast transits.
- **Stabilization.** Apply stabilization before extraction to reduce inter-frame jitter.
- **Gimbal attitude in EXIF.** Write camera pitch, roll, and yaw from telemetry so the
  reconstruction can use known orientation instead of solving for it, which should help on
  oblique frames.
- **Coverage reporting.** Estimate overlap from the telemetry track before processing, and warn
  when a segment is too sparse to reconstruct rather than discovering it after a long WebODM run.
- **Clock offset detection.** Estimate and correct video-to-telemetry time offset instead of
  assuming the two clocks agree.
- **Reprojection.** Emit orthophotos in Web Mercator (EPSG:3857) directly, since that is what
  the mapping tools downstream expect.

## License

MIT — use, copy, and modify freely, including commercially, as long as the copyright notice and
license text travel with the code. See [LICENSE](LICENSE).
