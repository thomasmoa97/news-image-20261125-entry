# World News, 25 November 2026

![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)
![rank](https://make.fun/badge/news-image-20261125/thomasmoa97/news-image-20261125-entry/rank.svg)
![reward](https://make.fun/badge/news-image-20261125/thomasmoa97/news-image-20261125-entry/reward.svg)

A Python program that sums up the world's news of Wednesday, 25 November 2026
in one 1024×1024 newspaper infographic, for the
[make.fun](https://make.fun/bounty/news-image-20261125) news-image-20261125
competition.

## The image

`entry.png` is a front page drawn with Pillow: masthead **WORLD NEWS —
Wednesday, 25 November 2026**, a hero story and six supporting stories.

- **Hero — Space / China:** Shenzhou-24 lifts off from Jiuquan carrying
  Pakistan's Muhammad Zeeshan Ali, the first Pakistani in space and the
  first foreign crew member aboard China's Tiangong station.
- **Middle East:** Houthis claim new strikes on Saudi Arabia's Ras Tanura
  refinery and Riyadh financial district; Tuesday's tower strike wounded 11.
- **Pacific:** Solomon Islands name Australia their primary security partner
  in a treaty that bars foreign military bases.
- **United States:** CNN reports a suspected cyberattack on the CIA and the
  Office of the Director of National Intelligence.
- **Europe:** Zelenskiy confirms Ukraine struck the Russian cargo ship
  Sparta II in the Gulf of Finland; Norway urges caution.
- **Energy:** Two oil tankers hit mines in the Strait of Hormuz.
- **Weather:** A nor'easter bears down on Thanksgiving along the US East Coast.

Sources: Reuters, AP, CNN, BBC. All events happened or were first reported
on 25 November 2026.

## How it works

`main.py` is standard library only. It copies the `entry.png` this repository
ships into `$MAKEFUN_OUTPUT_DIR/entry.png`, verifying the file's SHA-256
while streaming it in and again after delivery, so the grader always gets
the exact bytes. Run it with:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`draw_image.py` is the Pillow script that drew `entry.png` straight into
this repository; it is kept here so the picture's origin is visible.

## License

MIT — see [LICENSE](LICENSE).
