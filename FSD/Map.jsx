function Map(){
    const arr=[1,2,3,4,5]
    return(
        <>
            {arr.map((val) => {
                return <h2>Arrayelement={val*5}</h2>
            })
        }
        </>
    ) 
}
export default Map