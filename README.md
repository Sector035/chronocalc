# Chronocalc

I wrote this script after I was busy updating my article on chronolocation, which can be [found here](https://sector035.nl/articles/chronolocation-of-media).

It calculates the dates and times when the sun or moon is in a given position in the sky. It can be used during chronolocation tasks, to quickly find possible dates and times within a 15 minutes accuracy. For finding a more precise moment, one should use a tool like suncalc.org to find a closer match, or use the option `--accurate`.

## Installation

Install all the requirements first:

`pip install -r requirements.txt`

Or with the newest versions:

`python3.8 -m pip install -r requirements.txt`

## Usage

To determine the date and time, you need to have the following information already:
- The exact latitude and longitude of the location
- The year you want to calculate
- Height (altitude) of the sun or moon
- Direction (azimuth) of the sun or moon*

The script will pull the elevation information from an online source, and after this the script will iterate through a whole year, in 15 minute increments, and returns one of the following:

## Sun

Two dates on either side of the solstice, where the given altitude and azimuth matches the closest to the calculated time. If it's not possible to find a match, there might me two possibilities:
- The initial measurements are incorrect and the situation can't exist
- The location is extrmely close to the equator, and the sun moves too fast for the 15 minute increment

If the latitude given is close to the equator, about 2 degrees or less off, you can use the `--accurate` option. This will change the calculation interval to 2 minutes, given a better chance to find a possible match. This will take longer to retrieve a result, but if there is a match, it should be shown.

## Moon

To retrieve a list of dates where the moon is at a given position, use the optional argument `--moon`.

It will return all dates and times the moon is in the given position, and its illumination percentage. Since the moon can be in the same position multiple times a year, all dates that are within a are within a 2 degree limit of the altitude and azimuth are returned.

If there are no matches with the given parameter, it will return a message saying so. Change some variables, or check your findings, and run the script again. The `--accurate` argument has no use here.

### Examples

To find the dates where the sun is in a given position:

`python chronocalc.py -y 2020 -lat 50.9423 -lon 6.9579 -alt 32 -az 200`

Result:

```
+---------------------------+----------+---------+
|       Date and time       | Altitude | Azimuth |
+---------------------------+----------+---------+
| 2020-03-08T14:00:00+01:00 |  32.08   |  202.87 |
| 2020-10-05T14:30:00+02:00 |  32.09   |  200.58 |
+---------------------------+----------+---------+
```

Find all the dates where the moon is at a given position in the sky:

`python chronocalc.py -y 2018 -lat 50.9423 -lon 6.9579 -alt 30 -az 200 --moon`

Result:

```
+---------------------------+----------+---------+--------------+
|       Date and time       | Altitude | Azimuth | Illumination |
+---------------------------+----------+---------+--------------+
| 2018-01-08T08:15:00+01:00 | 31.28    | 218.99  |    56.6%     |
| 2018-01-22T19:15:00+01:00 | 28.95    | 221.78  |    28.0%     |
| 2018-02-05T07:00:00+01:00 | 28.28    | 219.48  |    73.7%     |
| 2018-03-04T04:45:00+01:00 | 30.69    | 219.79  |    94.1%     |
| 2018-03-18T15:45:00+01:00 | 31.54    | 219.73  |     1.4%     |
| 2018-04-14T14:45:00+02:00 | 28.95    | 220.78  |     2.9%     |
| 2018-04-28T02:15:00+02:00 | 30.16    | 219.45  |    95.3%     |
| 2018-05-12T13:15:00+02:00 | 31.91    | 220.0   |    11.5%     |
| 2018-05-25T00:15:00+02:00 | 31.48    | 220.87  |    78.6%     |
| 2018-06-08T11:15:00+02:00 | 28.91    | 221.16  |    34.2%     |
| 2018-06-21T23:00:00+02:00 | 28.62    | 219.23  |    65.3%     |
| 2018-07-18T21:00:00+02:00 | 29.86    | 220.99  |    39.3%     |
| 2018-08-02T07:45:00+02:00 | 30.6     | 219.83  |    75.1%     |
| 2018-08-29T05:45:00+02:00 | 29.26    | 219.47  |    93.1%     |
| 2018-09-11T17:30:00+02:00 | 29.16    | 221.32  |     5.1%     |
| 2018-09-26T04:30:00+02:00 | 31.86    | 221.75  |    98.8%     |
| 2018-10-23T02:15:00+02:00 | 31.01    | 218.37  |    96.8%     |
| 2018-11-05T13:00:00+01:00 | 28.59    | 221.58  |     5.8%     |
| 2018-11-18T23:15:00+01:00 | 28.16    | 219.37  |    79.9%     |
| 2018-12-02T10:45:00+01:00 | 31.51    | 219.53  |    24.7%     |
| 2018-12-16T21:45:00+01:00 | 30.99    | 218.8   |    63.4%     |
+---------------------------+----------+---------+--------------+
```