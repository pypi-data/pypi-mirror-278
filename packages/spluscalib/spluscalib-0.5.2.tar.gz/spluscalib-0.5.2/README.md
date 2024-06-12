# spluscalib
The photometric calibration pipeline of S-PLUS

[Purpose]
---------
This python package was developed exclusively for the photometric calibration of the S-PLUS observations and is fully dependent on the structure of the outputs of the S-PLUS reduction pipeline. Therefore, it is not intended for, and neither supports, any other uses.

The calibration is performed field by field (12-filters observations covering 1.4 x 1.4 deg). The main input of the pipeline are the 12 reduced (and likely co-added) fits images (and optionally 12 weight images) corresponding to the observations in the 12 filters of the S-PLUS photometric system. The pipeline performs the photometric calibration by applying a SED-fitting technique to AB-calibrated magnitudes of a reference catalog (fetched on the fly from the Vizier Database) and comparing the S-PLUS instrumental magnitudes with those predicted by the SEDs. The calibration zero-points are applied to the outputs of aperture photometry (from SExtractor) and/or PSF photometry (DoPHOT) and formatted in fits catalogs. 


[More details]
--------------
https://www.splus.iag.usp.br/


[Data Access]
-------------
https://splus.cloud/


[S-PLUS introduction paper and DR1]
-----------------------------------
https://ui.adsabs.harvard.edu/abs/2019MNRAS.489..241M/abstract

Mendes de Oliveira et al. (2019)
Monthly Notices of the Royal Astronomical Society, Volume 489, Issue 1, p.241-267


[S-PLUS calibration process description and DR2]
------------------------------------------------
https://ui.adsabs.harvard.edu/abs/2022MNRAS.511.4590A/abstract

Almeida-Fernandes et al. (2022)
Monthly Notices of the Royal Astronomical Society, Volume 511, Issue 3, pp.4590-4618


[KNOWN BUGS]
------------
- Diagnostic step does not work with GAIADR2 extinction correction


<br>
<br>

---
---
[Running spluscalib on docker]
------------------------------

### 1. Install Docker and docker-compose

First, you need to install Docker on your computer. You can download it from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).

And then, you need to install docker-compose. You can download it from [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/).

### 2. Set up the folders

Inside ./server/docker_folders you will find the folders that will be mounted in the docker-compose image. You can add the files that you want to process in the input folder and the results will be saved in the output folder.

The structure of the folders is the following:

```
./server/docker_folders/
│
├── media/
│   ├── CALIB/
│   │   ├── config/
│   
├── temp/ (not used yet)

```

Note that the media folder may be a symbolic link to the folder where you have the data that you want to process, or to a drive with enough space to store the results.

### 3. Build and Run the docker-compose image

You can build the docker-compose image by running the following command in the terminal:

```bash
docker-compose build
```

You can run the docker-compose image by running the following command in the terminal:

```bash
docker-compose up
```


### 4. Control the server

You can access the server by doing some GET and POST requests to the following URLs:

- ### Check if the server is processing data
```
http://localhost:8003/is_running/ (GET)
```
---
- ### Start the calibration process for one field
```
http://localhost:8003/process_field/ (POST)
```

Example of the body of the POST request
```
{
    "config_file": "iDR5_3_Main.conf", #(conf in the config folder)
    "field": "STRIPE82-0001",
}
```

- ### Start the calibration process for a list of fields
```
http://localhost:8003/process_field_list/ (POST)
````

Example of the body of the POST request
```
{
    "fields": ["HYDRA_0012", "HYDRA_0049"],
    "config_file": "iDR5_3_Main.conf"
}
```

---
- ### Get the logs of the calibration process
```
http://localhost:8003/get_logs/ (GET)
```
