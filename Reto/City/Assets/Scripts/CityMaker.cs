/* Sylvia Fernanda Colomo Fuente - A01781983*/

using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class CityMaker : MonoBehaviour
{
    public List<GameObject> buildingPrefabs;//lista de edificios para que haya variedad
    [SerializeField] TextAsset layout;//archivo txt con el mapa
    [SerializeField] GameObject road;//prefab del camino
    [SerializeField] GameObject semaforo;//prefab del semaforo
    [SerializeField] GameObject destiny;//prefab del edificio destino
    [SerializeField] int tileSize;//tamaño de la tile

    private int edificio;// va a guardar el edificio random seleccionado para luego saber cuál instanciar

    // Start is called before the first frame update
    void Start()
    {
        MakeTiles(layout.text);//llama a la funcion que crea el mapa
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void MakeTiles(string tiles)
    {
        int x = 0;
        int y = tiles.Split('\n').Length -1;

        Vector3 position;//variable para guardar la posicion de la tile
        GameObject tile;//variable para guardar el prefab que se va a instanciar

        for (int i=0; i<tiles.Length; i++) {

            //ROAD
            if (tiles[i] == 'v' || tiles[i] == '^') {
                //estas casillas van arriba o abajo y por default el tile apunta a esas direcciones
                position = new Vector3(x * tileSize, 0, y * tileSize);//multiplicamos por el tamaño de la tile para que se vayan colocando una al lado de la otra
                tile = Instantiate(road, position, Quaternion.identity);//instanciamos el prefab del camino
                tile.transform.parent = transform;//Aquí esta instancia se vuelve hija de City (el gameobject en nuestro unity que tiene este script)
                x += 1;//con esto nos movemos a la siguiente tile
            } else if (tiles[i] == '>' || tiles[i] == '<') {
                //estas casillas van a la derecha o izquierda por lo que giramos el tile 90 grados 
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(road, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } 
            //SEMAFORO
            else if ((tiles[i] == 'S')||(tiles[i] == 'T')) {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(road, position, Quaternion.identity);
                tile.transform.parent = transform;
                tile = Instantiate(semaforo, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if ((tiles[i] == 's')||(tiles[i] == 't') ){
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(road, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                tile = Instantiate(semaforo, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } 
            //DESTINO
            else if (tiles[i] == 'D') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(destiny, position, Quaternion.identity);
                //tile.GetComponent<Renderer>().materials[0].color = Color.red;
                tile.transform.localScale = new Vector3(.1f, Random.Range(0.1f, 0.15f), .1f);//modifica el tamaño del edificio
                tile.transform.parent = transform;
                x += 1;
            //EDIFICIOS
            } else if (tiles[i] == '#') {
                edificio=Random.Range(0,buildingPrefabs.Count());
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(buildingPrefabs[edificio], position, Quaternion.identity);
                tile.transform.localScale = new Vector3(.1f, Random.Range(0.1f, 0.15f), .1f);
                tile.transform.parent = transform;
                x += 1;
            //Vacio
            }else if (tiles[i] == '\n') {//si hay un salto de linea, regresamos a la posicion inicial en x y bajamos una posicion en y
                x = 0;
                y -= 1;
            }
        }

    }
}
