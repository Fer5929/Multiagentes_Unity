using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BasicLerp : MonoBehaviour
{
    [SerializeField] Vector3 startpos;
    [SerializeField] Vector3 finalpos;
    [Range (0.0f, 1.0f)]
    [SerializeField] float t;
    [SerializeField] float moveTime;
    float elapsedTime = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
        

    }

    // Update is called once per frame
    void Update()
    {
        t=elapsedTime/moveTime;

        //Use a function to smooth the movement
        t = t * t * (3.0f - 2.0f * t); //acelera y frene 


        Vector3 position = startpos + (finalpos - startpos) * t;

        //Move the object using Unity transforms
        transform.position = position;
        Matrix4x4 move = HW_Transforms.TranslationMat(position.x, position.y, position.z);

        elapsedTime += Time.deltaTime;

        if (elapsedTime > moveTime)
        {   //elapsedTime=moveTime; se detiene en el punto final
            elapsedTime = 0.0f;

            //Swap the start and final positions
            Vector3 temp = finalpos;
            finalpos = startpos;
            startpos = temp;
        }
    }
}
