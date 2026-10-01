using System; using System.Collections.Generic; using System.Linq; using System.Text; using System.Threading.Tasks; 
 
namespace Practical_2 
{ 
    class Overloading 
    { 
        public void swap(ref int n, ref int m) 
        {             int t;             t = n;             n = m;             m = t; 
        } 
        public void swap(ref float f1, ref float f2) 
        { 
            float f;             f = f1;             f1 = f2;             f2 = f; 
        } 
        class program 
        { 
            static void Main(string[] args) 
            { 
                Console.WriteLine("TY-IT 719_Anuj");                  Overloading objOverloading = new Overloading(); 
                int n = 54, m = 34;                 objOverloading.swap(ref n, ref m);                 Console.WriteLine("N=" + n + "\tM=" + m);                 float f1 = 19.5f, f2 = 69.4f;                 objOverloading.swap(ref f1, ref f2); 
                Console.WriteLine("F1=" + f1 + "\tF2=" + f2); 
                Console.ReadKey(); 
            } 
        } 
    } 
} 
