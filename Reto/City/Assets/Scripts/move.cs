//S Fernanda Colomo F - A01781983
//Ian Luis Vázquez Morán - A01027225
//Codigo usado para el movimiento del carro, la rotación e instancación de sus ruedas 
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class move : MonoBehaviour
{
    double displacement=.1;
    float angle;
    AXIS rotationAxis = AXIS.Y;
    [SerializeField] AXIS rotationAxiswheels;

    Mesh mesh;//Carro
    Mesh meshwheel1;//ruedas 1-4
    Mesh meshwheel2;
    Mesh meshwheel3;
    Mesh meshwheel4;

    [SerializeField] GameObject wheel;//rueda a usar 
    //posiciones de las ruedas
    [SerializeField] Vector3 posicion_wheel1;
    [SerializeField] Vector3 posicion_wheel2;
    [SerializeField] Vector3 posicion_wheel3;
    [SerializeField] Vector3 posicion_wheel4;
    [SerializeField] float angle_Right_wheels;
    [SerializeField] AXIS rotationAxis_Right_wheels;
    [SerializeField] float angle_Left_wheels;
    [SerializeField] AXIS rotationAxis_Left_wheels;
    [SerializeField] Vector3 scale;

//vertices para las ruedas
    Vector3[] baseVertices;
    Vector3[] baseVerticeswheel1;
    Vector3[] baseVerticeswheel2;
    Vector3[] baseVerticeswheel3;
    Vector3[] baseVerticeswheel4;
    Vector3[] newVertices;
    Vector3[] newVerticeswheel1;
    Vector3[] newVerticeswheel2;
    Vector3[] newVerticeswheel3;
    Vector3[] newVerticeswheel4;
    float wheelvel;

    Vector3 startp;//posicion inicial del carro
    Vector3 stoppos;//posicion final del carro

    Vector3 prevPositions;
    float t;
    float current;
    float motionTime=1f;
    Vector3 result;
    

    // Start is called before the first frame update
    void Start()
    {
        //instancia las ruedas 
        GameObject wheel1=Instantiate(wheel, new Vector3(0, 0, 0), Quaternion.identity);
        wheel1.name = gameObject.name + "wheel1";
        GameObject wheel2=Instantiate(wheel, new Vector3(0, 0, 0), Quaternion.identity);
        wheel2.name = gameObject.name + "wheel2";
        GameObject wheel3=Instantiate(wheel, new Vector3(0, 0, 0), Quaternion.identity);
        wheel3.name = gameObject.name + "wheel3";
        GameObject wheel4=Instantiate(wheel, new Vector3(0, 0, 0), Quaternion.identity);
        wheel4.name = gameObject.name + "wheel4";

        //obtiene las mallas de los objetos
        mesh=GetComponentInChildren<MeshFilter>().mesh;
        meshwheel1=wheel1.GetComponentInChildren<MeshFilter>().mesh;
        meshwheel2=wheel2.GetComponentInChildren<MeshFilter>().mesh;
        meshwheel3=wheel3.GetComponentInChildren<MeshFilter>().mesh;
        meshwheel4=wheel4.GetComponentInChildren<MeshFilter>().mesh;
        //obtiene los vertices de los objetos
        baseVertices=mesh.vertices;
        baseVerticeswheel1 = meshwheel1.vertices;
        baseVerticeswheel2 = meshwheel2.vertices;
        baseVerticeswheel3 = meshwheel3.vertices;
        baseVerticeswheel4 = meshwheel4.vertices;


        //se crea un arreglo para guardar los vertices
        newVertices= new Vector3[baseVertices.Length];
        newVerticeswheel1= new Vector3[baseVerticeswheel1.Length];
        newVerticeswheel2= new Vector3[baseVerticeswheel2.Length];
        newVerticeswheel3= new Vector3[baseVerticeswheel3.Length];
        newVerticeswheel4= new Vector3[baseVerticeswheel4.Length];
        // Copia las coordenadas
        for (int i=0; i<baseVertices.Length; i++){
            newVertices[i]=baseVertices[i];
        }
        
        for (int i=0; i<baseVerticeswheel1.Length; i++){
            newVerticeswheel1[i]=baseVerticeswheel1[i];
            newVerticeswheel2[i]=baseVerticeswheel2[i];
            newVerticeswheel3[i]=baseVerticeswheel3[i];
            newVerticeswheel4[i]=baseVerticeswheel4[i];
        }
        
        Dotransform();//se llama a la funcion para mover el carro
        
    }

    // Update is called once per frame
    void Update()
    {
        Dotransform();
    }
    public void Positions(Vector3 npos){//obtiene la posición en la que se encuentra el carro
       startp=stoppos;
       stoppos=npos;
       result = stoppos - startp;
       if (result.x!=0 || result.z!=0){
        angle=Mathf.Atan2(result.x, result.z);
        angle=angle*Mathf.Rad2Deg;
        displacement=.1;
        }
        else{
            displacement=0;
        }
       current=0;
    }
    public Vector3 returnpos(){//regresa la posición del carro en el tiempo determinado
        current += Time.deltaTime;
        t=current/motionTime;
        if (t>1){
            t=1;
        }
        
        return startp + (stoppos-startp)*t;
    }


    void Dotransform(){//hace las transformaciones del carro en base a returnpos
        Vector3 pos;
        pos =returnpos();
        Matrix4x4 move=HW_Transforms.TranslationMat(pos.x,
                                                    pos.y,
                                                    pos.z);
            
        Matrix4x4 scalecar=HW_Transforms.ScaleMat(0.1810022f,
                                                    0.1810022f,
                                                    0.1810022f);
        /*Matrix4x4 moveOrigin=HW_Transforms.TranslationMat(-displacement.x,
                                                    -displacement.y,
                                                    -displacement.z);

        Matrix4x4 moveObject=HW_Transforms.TranslationMat(displacement.x,
                                                    displacement.y,
                                                    displacement.z);*/

        Matrix4x4 rotate=HW_Transforms.RotateMat(angle,rotationAxis);

        //Combine all matrix in single one
        Matrix4x4 composite = move*rotate*scalecar;
        Matrix4x4 composites = move*rotate*scalecar;

        //Multiply each vertex in the composite matrix
        for (int i=0; i<newVertices.Length; i++){
            Vector4 temp=new Vector4(baseVertices[i].x,
                                     baseVertices[i].y,
                                     baseVertices[i].z,
                                     1);
            newVertices[i]=composite * temp;
        }


        //remplace vertices in the mesh
        mesh.vertices=newVertices;
        mesh.RecalculateNormals();
        mesh.RecalculateBounds();
        
        Matrix4x4 scales=HW_Transforms.ScaleMat(scale.x,scale.y,scale.z);
        Matrix4x4 rotateright=HW_Transforms.RotateMat(angle_Right_wheels, rotationAxis_Right_wheels);
        Matrix4x4 rotateleft=HW_Transforms.RotateMat(angle_Left_wheels, rotationAxis_Left_wheels);

        Matrix4x4 RightUp = HW_Transforms.TranslationMat(posicion_wheel3.x, posicion_wheel3.y, posicion_wheel3.z);
        Matrix4x4 RightBack = HW_Transforms.TranslationMat(posicion_wheel4.x, posicion_wheel4.y, posicion_wheel4.z);
        Matrix4x4 LeftUp = HW_Transforms.TranslationMat(posicion_wheel2.x, posicion_wheel2.y, posicion_wheel2.z);
        Matrix4x4 LeftBack = HW_Transforms.TranslationMat(posicion_wheel1.x, posicion_wheel1.y, posicion_wheel1.z);

        Matrix4x4 Right = scales * rotateright;
        Matrix4x4 Left = scales * rotateleft;
        wheelvel=(float)displacement*360;
        print(displacement);
        Matrix4x4 rotatewheel=HW_Transforms.RotateMat(wheelvel*Time.time,rotationAxiswheels);
        Matrix4x4 rotatewheel2=HW_Transforms.RotateMat(-wheelvel*Time.time,rotationAxiswheels);
        // Aplicar transformaciones de las ruedas en relación con el objeto principal
        
        Matrix4x4 RightUpcomposite =RightUp * Right;
        Matrix4x4 newcomposite =composites* RightUpcomposite*rotatewheel2;

        Matrix4x4 RightBackcomposite = RightBack * Right;
        Matrix4x4 newcomposite2 =composites* RightBackcomposite*rotatewheel2;

        Matrix4x4 LeftUpcomposite =LeftUp * Left;
        Matrix4x4 newcomposite3 =composites* LeftUpcomposite*rotatewheel;

        Matrix4x4 LeftBackcomposite =LeftBack * Left ;
        Matrix4x4 newcomposite4 =composites* LeftBackcomposite*rotatewheel;

        // Aplicar transformaciones a las coordenadas de las ruedas
        for (int i = 0; i < baseVerticeswheel1.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticeswheel1[i].x, baseVerticeswheel1[i].y, baseVerticeswheel1[i].z, 1);
            newVerticeswheel1[i] = newcomposite * temp;
        }
        for (int i = 0; i < baseVerticeswheel2.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticeswheel2[i].x, baseVerticeswheel2[i].y, baseVerticeswheel2[i].z, 1);
            newVerticeswheel2[i] = newcomposite2 * temp;
        }

        for (int i = 0; i < baseVerticeswheel3.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticeswheel3[i].x, baseVerticeswheel3[i].y, baseVerticeswheel3[i].z, 1);
            newVerticeswheel3[i] = newcomposite3 * temp;
        }

        for (int i = 0; i < baseVerticeswheel4.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticeswheel4[i].x, baseVerticeswheel4[i].y, baseVerticeswheel4[i].z, 1);
            newVerticeswheel4[i] = newcomposite4 * temp;
        }

        // Aplicar nuevas coordenadas a las mallas de las ruedas
        meshwheel1.vertices = newVerticeswheel1;
        meshwheel1.RecalculateNormals();
        meshwheel1.RecalculateBounds();

        meshwheel2.vertices = newVerticeswheel2;
        meshwheel2.RecalculateNormals();
        meshwheel2.RecalculateBounds();

        meshwheel3.vertices = newVerticeswheel3;
        meshwheel3.RecalculateNormals();
        meshwheel3.RecalculateBounds();

        meshwheel4.vertices = newVerticeswheel4;
        meshwheel4.RecalculateNormals();
        meshwheel4.RecalculateBounds();


    }
}
