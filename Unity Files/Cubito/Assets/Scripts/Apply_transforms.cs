//Sylvia Fernanda Colomo Fuente A01781983

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Apply_transforms : MonoBehaviour
{
    //para el carro se declara el vector de desplazamiento, el angulo y el eje de rotacion
    [SerializeField] Vector3 displacement;
    [SerializeField] float angle;
    //este ángulo será calculado más adelante para evitar tener que calcularlo manualmente 
    [SerializeField] AXIS rotationAXIS;

    //Ruedas, se van a instanciar, se usa un gameobject a instanciar
    //en el inspector se arrastrará el modelo de la rueda a usar 
    [SerializeField] GameObject wheelModel;

    Mesh mesh;//mesh del carro
    Vector3[] vertices;
    Vector3[] newVertices;
    //uso de vertices y newvertices para las transformaciones

    [SerializeField] Wheel[] wheel;//Lista de ruedas (clase ya definida)

    // Start is called before the first frame update
    void Start()
    {
        //Se obtiene el mesh del carro y en base a eso se obtienen los vertices
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        vertices = mesh.vertices;

        //Create a copy to testing the vertices
        newVertices = new Vector3[vertices.Length];
        System.Array.Copy(vertices, newVertices, vertices.Length);

        //Intancia las ruedas 
        //por cada elemento de tipo Wheel en la lista se instancia un gameobject con sus debidos atributos 
        //al igual que el carro se usa una mesh, vertices y newvertices
        for(int i = 0; i<wheel.Length; i++){
            GameObject temp = Instantiate(wheelModel, new Vector3(0,0,0), Quaternion.identity);

            //de cada rueda en la lista se obtiene su mesh, vertices y newvertices
            wheel[i].mesh = temp.GetComponentInChildren<MeshFilter>().mesh;
            wheel[i].vertices = wheel[i].mesh.vertices;
            wheel[i].newVertices = new Vector3[wheel[i].vertices.Length];
            System.Array.Copy(wheel[i].vertices, wheel[i].newVertices, wheel[i].vertices.Length);
        }


    }
    
    // Update is called once per frame
    void Update()
    {
        DoTransform();
        //se coloca el método en Update ya que se quiere que se actualice cada frame
    }

    void DoTransform(){
        //matrices a usar 
        //movimiento
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x *Time.time,
                                                      displacement.y *Time.time,
                                                      displacement.z *Time.time);

        angle =Mathf.Atan2(displacement.z, displacement.x) * Mathf.Rad2Deg;
        //en caso de tener dos desplazamientos se hará esta operación para obtener el ángulo de rotación
        
        Matrix4x4 rotate = HW_Transforms.RotateMat(angle, rotationAXIS);//matrix de rotación
        Matrix4x4 composite =  move*rotate;//matriz compuesta en la cual primero se rota el carro y después se mueve en esa dirección
        

        //matrices para las ruedas, una matrix de traslación para cada rueda
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
        //aquí se mueve relativamente al carro, por eso se multiplica por la matriz compuesta del carro


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
        //normales para la lista de ruedas 
        for (int i = 0; i<wheel.Length; i++){
            wheel[i].mesh.vertices = wheel[i].newVertices;
            wheel[i].mesh.RecalculateNormals();
        }

    }

}

//Clase de la rueda
[System.Serializable] 
public class Wheel{

    //se declara la mesh, los vertices y los newvertices para cada rueda
    public Mesh mesh;
    public Vector3[] vertices;
    public Vector3[] newVertices;

    //se declara la posición y el ángulo de rotación para cada rueda
    [SerializeField] public Vector3 position;
    [SerializeField] public float rotation;

    public Wheel(Vector3 pos){
        position = pos;
    }
}

    

