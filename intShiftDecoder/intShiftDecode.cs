using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace decodeints
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.InputEncoding = Encoding.Unicode;
            Console.OutputEncoding = Encoding.Unicode;

            
            Console.WriteLine("Enter encoded string: ");
            string inputString = Console.ReadLine();
            Console.WriteLine("Enter Int Shift Value: ");
            long intValue = Convert.ToInt64(Console.ReadLine());

            StringBuilder stringbuilder = new StringBuilder();
            foreach (char c in inputString.ToCharArray())
            {
                stringbuilder.Append((char)((int)c - intValue));
            }
            Console.WriteLine(stringbuilder.ToString());
        }
    }
}
