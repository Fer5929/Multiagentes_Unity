using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightBehavior : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject GreenLight;
    public GameObject GreenLight2;
    public GameObject RedLight;
    public GameObject RedLight2;

    void Start()
    {
        
    }

    public void toggleLights(bool state){
        if (state == true){
            GreenLight.SetActive(true);
            GreenLight2.SetActive(true);
            RedLight.SetActive(false);
            RedLight2.SetActive(false);
        } else {
            GreenLight.SetActive(false);
            GreenLight2.SetActive(false);
            RedLight.SetActive(true);
            RedLight2.SetActive(true);
        }
    }
    

    // Update is called once per frame
    void Update()
    {
        
    }
}
