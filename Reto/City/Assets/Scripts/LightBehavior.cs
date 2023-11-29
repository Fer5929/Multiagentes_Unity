using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightBehavior : MonoBehaviour
{
    // Script que modifica el color de las luces en un tiempo determinado
    public GameObject light;//luz

    //variables para saber cuando cambiar de luz
    private bool red;

    private bool green;

    public int change;//tiempo de cambio

    public  void Start()
    {
        //se inicia con todos en verde
        red = false;
        green = true;
    }

    // Update is called once per frame
    void Update()
    {
        if (red==true)
        {
            light.GetComponent<Light>().color = Color.red;//se cambia el color de la luz a rojo
            StartCoroutine(redlight());//se llama a la corrutina para cambiar a verde

        }
        if (green==true)
        {
            light.GetComponent<Light>().color = Color.green;//se cambia el color de la luz a verde
            StartCoroutine(greenlight());//se llama a la corrutina para cambiar a rojo
        }
    }

    IEnumerator greenlight()
    {
        yield return new WaitForSeconds(change);//se espera el tiempo de cambio
        //se cambia el estado de las variables
        green = false;
        red = true;
    }

    IEnumerator redlight()
    {
        yield return new WaitForSeconds(change);//se espera el tiempo de cambio
        //se cambia el estado de las variables
        green = true;
        red = false;
    }
}
