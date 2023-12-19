// Define function to reduce regions and summarize pixel values
// to get mean LST for different cases.
function polygonMean(feature){

    // Calculate spatial mean value of LST for each case
    // making sure the pixel values are converted to °C from Kelvin.
    var reducedLstUrb=lstFinal.subtract(273.15).updateMask(notWater)
        .reduceRegion({
            reducer: ee.Reducer.mean(),
            geometry: feature.geometry(),
            scale: 30
        });
    var reducedLstUrbMask=lstFinal.subtract(273.15).updateMask(
            notWater)
        .updateMask(urbanUrban)
        .reduceRegion({
            reducer: ee.Reducer.mean(),
            geometry: feature.geometry(),
            scale: 30
        });
    var reducedLstUrbPix=lstFinal.subtract(273.15).updateMask(
            notWater)
        .updateMask(urbanUrban)
        .reduceRegion({
            reducer: ee.Reducer.mean(),
            geometry: feature.geometry(),
            scale: 500
        });
    var reducedLstLandsatUrbPix=landsatComp.updateMask(notWater)
        .updateMask(urbanUrban)
        .reduceRegion({
            reducer: ee.Reducer.mean(),
            geometry: feature.geometry(),
            scale: 30
        });
    var reducedLstRurPix=lstFinal.subtract(273.15).updateMask(
            notWater)
        .updateMask(urbanNonUrban)
        .reduceRegion({
            reducer: ee.Reducer.mean(),
            geometry: feature.geometry(),
            scale: 500
        });
    var reducedLstLandsatRurPix=landsatComp.updateMask(notWater)
        .updateMask(urbanNonUrban)
        .reduceRegion({
            reducer: ee.Reducer.mean(),
            geometry: feature.geometry(),
            scale: 30
        });