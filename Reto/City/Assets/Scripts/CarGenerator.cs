//S Fernanda Colomo F - A01781983
//Ian Luis Vázquez Morán - A01027225
//Codigo usado para la generación de carros de manera random
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarGenerator : MonoBehaviour
{
    //Carros posibles
    [SerializeField] GameObject CarType1;
    [SerializeField] GameObject CarType2;
    [SerializeField] GameObject CarType3;
    [SerializeField] GameObject CarType4;
    [SerializeField] GameObject CarType5;
    [SerializeField] Vector3 pos;

    private GameObject prefab;
    
    // Start is called before the first frame update
    void Start()
    {

        GenerarObjeto();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
     void GenerarObjeto()
    {
        // Genera un número aleatorio entre 1 y 5 (ambos inclusive)
        int randomIndex = Random.Range(1, 6);

        // Usa el número aleatorio para seleccionar uno de los objetos
        switch (randomIndex)
        {
            case 1:
                prefab = CarType1;
                break;
            case 2:
                prefab = CarType2;
                break;
            case 3:
                prefab = CarType3;
                break;
            case 4:
                prefab = CarType4;
                break;
            case 5:
                prefab = CarType5;
                break;
            default:
                Debug.LogError("Número aleatorio fuera de rango");
                break;
        }
        // Instancia el prefab en la posición y rotación deseadas
        Instantiate(prefab, new Vector3(pos.x, pos.y, pos.z), Quaternion.identity);
    }
}
