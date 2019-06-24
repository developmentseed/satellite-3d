# Satellite-3d

Using rio-tiler-mvt to create Mapbox satellite + Elevation 3d Vector tiles.

![](https://user-images.githubusercontent.com/10407788/59771301-700a5680-9277-11e9-93ed-f817d6055648.jpg)

More on [COG Talk](https://medium.com/devseed/search?q=cog%20talk) blog posts

## Deployment

#### Package Lambda

Create `package.zip`

```bash
$ docker-compose build --no-cache
$ docker-compose run --rm package
```

#### Deploy to AWS

```bash
$ npm install

# You'll need to have "MapboxAccessToken" set to a valid mapbox token to download mapbox.satellite tiles
$ export MapboxAccessToken={YOU MAPBOX TOKEN}

$ sls deploy
```

## Demo

[index.html](/index.html) (Needs to be edited to add enpoint and mapbox token)

## About
Created by [Development Seed](<http://developmentseed.org>)
