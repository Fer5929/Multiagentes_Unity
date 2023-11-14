using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Apply_transforms : MonoBehaviour
{
    //para el carro
    [SerializeField] Vector3 displacement;
    [SerializeField] float angle;
    [SerializeField] AXIS rotationAXIS;

    //Ruedas, se van a instanciar, se usa un gameobject a instanciar
    [SerializeField] GameObject wheelModel;

    Mesh mesh;
    Vector3[] vertices;
    Vector3[] newVertices;
    //uso de vertices y newvertices para las transformaciones

    [SerializeField] Wheel[] wheel;//Lista de ruedas 

    // Start is called before the first frame update
    void Start()
    {
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        vertices = mesh.vertices;

        //Create a copy to testing the vertices
        newVertices = new Vector3 [vertices.Length];
        for (int i = 0; i<vertices.Length; i++){
            newVertices[i] = vertices[i];
        }

        //Intancia las ruedas 
        for(int i = 0; i<wheel.Length; i++){
            GameObject temp = Instantiate(wheelModel, new Vector3(0,0,0), Quaternion.identity);

            //de cada rueda en la lista se obtiene su mesh, vertices y newvertices
            wheel[i].mesh = temp.GetComponentInChildren<MeshFilter>().mesh;
            wheel[i].vertices = wheel[i].mesh.vertices;
            wheel[i].newVertices = new Vector3[wheel[i].vertices.Length];
            for(int j = 0; j<wheel[i].vertices.Length; j++){ //Create a copy of the vertices
                wheel[i].newVertices[j] = wheel[i].vertices[j];
            }
        }


    }

    // Update is called once per frame
    void Update()
    {
        DoTransform();
    }

    void DoTransform(){
        //matrices a usar 
        //movimiento
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x *Time.time,
                                                      displacement.y *Time.time,
                                                      displacement.z *Time.time);
        Matrix4x4 rotate = HW_Transforms.RotateMat(angle, rotationAXIS);
        Matrix4x4 composite = rotate * move;
        //en unity se lee al revés ya que se habla de operaciones con matrices por lo tanto composite se mueve y luego rota

        //matrices para las ruedas 
        Matrix4x4 W1 = HW_Transforms.TranslationMat(wheel[0].position.x,
                                                                    wheel[0].position.y,
                                                                    wheel[0].position.z);

        Matrix4x4 W2 = HW_Transforms.TranslationMat(wheel[1].position.x,
                                                                    wheel[1].position.y,
                                                                    wheel[1].position.z);

        Matrix4x4 W3 = HW_Transforms.TranslationMat(wheel[2].position.x,
                                                                    wheel[2].position.y,
                                                                    wheel[2].position.z);

        
        Matrix4x4 W4 = HW_Transforms.TranslationMat(wheel[3].position.x,
                                                                    wheel[3].position.y,
                                                                    wheel[3].position.z);

        //matrix de rotacion para las ruedas, con que se cree una se puede aplicar despues para todas 
        Matrix4x4 rotate_wheel1 = HW_Transforms.RotateMat(wheel[0].rotation * Time.time, AXIS.X);
        

        //Apply the composite for each wheel
        Matrix4x4 wheel_composite1 =  composite * W1 * rotate_wheel1;  
        Matrix4x4 wheel_composite2 = composite * W2 * rotate_wheel1;
        Matrix4x4 wheel_composite3 = composite * W3 * rotate_wheel1;
        Matrix4x4 wheel_composite4 =  composite * W4 * rotate_wheel1;


        //Carro
        for(int i = 0; i<vertices.Length; i++){
            Vector4 temp = new Vector4(vertices[i].x,
                                       vertices[i].y,
                                       vertices[i].z,1);
            newVertices[i] = composite * temp;
        }

        
        //Ruedas
        for(int i = 0; i<wheel[0].vertices.Length; i++){
            Vector4 temp = new Vector4(wheel[0].vertices[i].x,
                                       wheel[0].vertices[i].y,
                                       wheel[0].vertices[i].z,1);

            wheel[0].newVertices[i] = wheel_composite1 * temp;

        }

        for(int i = 0; i <wheel[1].vertices.Length; i++){
            Vector4 temp = new Vector4(wheel[1].vertices[i].x,
                                       wheel[1].vertices[i].y,
                                       wheel[1].vertices[i].z,1);

            wheel[1].newVertices[i] = wheel_composite2 * temp;
        }

        for(int i = 0; i <wheel[2].vertices.Length; i++){
            Vector4 temp = new Vector4(wheel[2].vertices[i].x,
                                       wheel[2].vertices[i].y,
                                       wheel[2].vertices[i].z,1);

            wheel[2].newVertices[i] = wheel_composite3 * temp;
        }

        for(int i = 0; i <wheel[3].vertices.Length; i++){
            Vector4 temp = new Vector4(wheel[3].vertices[i].x,
                                       wheel[3].vertices[i].y,
                                       wheel[3].vertices[i].z,1);

            wheel[3].newVertices[i] = wheel_composite4 * temp;
        }

        //Normales para las ruedas y el carro
        mesh.vertices = newVertices;
        mesh.RecalculateNormals();
        for (int i = 0; i<wheel.Length; i++){
            wheel[i].mesh.vertices = wheel[i].newVertices;
            wheel[i].mesh.RecalculateNormals();
        }

    }

}

//Clase de la rueda
[System.Serializable] 
public class Wheel{

    public Mesh mesh;
    public Vector3[] vertices;
    public Vector3[] newVertices;

    [SerializeField] public Vector3 position;
    [SerializeField] public float rotation;

    public Wheel(Vector3 pos){
        position = pos;
    }
}

    

