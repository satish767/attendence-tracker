using System;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            int num1, num2, num3, num4, prod;
            Console.Write("Enter number 1:");
            num1 = Int32.Parse(Console.ReadLine());
            Console.Write("Enter number 2:");
            num2 = Convert.ToInt32(Console.ReadLine());
            Console.Write("Enter number 3:");
            num3 = Convert.ToInt32(Console.ReadLine());
            Console.Write("Enter number 4:");
            num4 = Convert.ToInt32(Console.ReadLine());
            prod = num1 * num2 * num3 * num4;
            Console.WriteLine(num1 + "*" + num2 + "*" + num3 + "*" + num4 + "=" + prod);
            Console.Write("735_Chirag Joshi");
            Console.ReadKey();
        }
    }
}
