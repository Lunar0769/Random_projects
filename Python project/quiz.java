import java.util.*;

class Participant implements Runnable 
{
    String name;
    int age;
    String contactNumber;
    List<Character> answers = new ArrayList<>();
    
    
    public Participant(String name, int age, String contactNumber) {
        this.name = name;
        this.age = age;
        this.contactNumber = contactNumber;
    }

    public String getName() 
    {
        return name;
    }

    public int getAge() 
    {
        return age;
    }

    public String getContactNumber() 
    {
        return contactNumber;
    }

    public List<Character> getAnswers() 
    {
        return answers;
    }

    public void run() 
    {
        System.out.println("Participant: " + name + ", Age: " + age + ", Contact Number: " + contactNumber);
        Scanner scanner = new Scanner(System.in);

        synchronized (this) 
        {
            System.out.println();
            System.out.println();
            System.out.println("Hello "+name+" Here are questions for Quiz");
            System.out.println("Q.1. National bird of INDIA..(A) Peacock (B) Sparrow (C) Duck (D) Owl ");
            System.out.println("Q.2  Independence year of INDIA..(A) 1955 (B) 1947 (C) 1999 (D) 1929 ");
            System.out.println("Q.3  Gandhi Jayanti is on......(A) 2nd Oct (B) 5th Oct (C) 9th Oct (D) 7th Oct ");
            System.out.println("Q.4  Count of states in INDIA..(A) 17 (B) 21 (C) 25 (D) 28 ");
            System.out.println("Q.5  how many continents are there in the world..(A) 5 (B) 6 (C) 7 (D) 8 ");

            for (int i = 1; i <= 5; i++) 
            {
                System.out.print("Enter your answer for Question " + i + ": ");
                char answer = scanner.nextLine().charAt(0);
                answers.add(answer);
            }

        }
        scanner.close();
    }
}

class QuizGame 
{
    public static void main(String[] args) throws InterruptedException 
    {
        Scanner scanner = new Scanner(System.in);
        ArrayList<Participant> participants = new ArrayList<>();
        Stack<Character> correctAnswers = new Stack<>();
        correctAnswers.push('A');
        correctAnswers.push('B');
        correctAnswers.push('A');
        correctAnswers.push('D');
        correctAnswers.push('C');

        System.out.println("Enter participants details");
        for(int i=1; i<=3;i++)
        {
            System.out.println();
            System.out.println("Enter name of participant "+i);
            String name = scanner.nextLine();
           // sc.nextInt();
            System.out.println("Enter age of participant "+i);
            int age = scanner.nextInt();
            scanner.nextLine();
            boolean t = true;
            String  mobileNumber;
            while(t)
            {
             System.out.println("Enter valid mobile number 10 digit & starting fron 9");
              mobileNumber= scanner.nextLine();
              if(mobileNumber.length()==10 && mobileNumber.charAt(0)==('9'))
              {
                System.out.println("Mobile number confirm");
                Participant p = new Participant(name, age ,mobileNumber);
                participants.add(p);
                t=false;
              }
              else{
                System.out.println("please enter a valid mobile number");
                t=true;
              }
            }
        }

        Collections.sort(participants,Comparator.comparing(Participant::getAge));

        List<Thread> threads = new ArrayList<>();
        
        for (Participant participant : participants) 
        {
            Thread thread = new Thread(participant);
            threads.add(thread);
            thread.start();
            thread.join();
        }

        for (Thread thread : threads) 
        {
            thread.join();
        }

        int highestScore = 0;
        String winner = "";

        System.out.println("----------------Results:------------------");
        for (Participant participant : participants) {
            int score = calculateScore(participant.getAnswers(), correctAnswers);
            System.out.println("Participant: " + participant.getName() + ", Age: " + participant.getAge() + ", Contact Number: " + participant.getContactNumber() + ", Score: " + score);

            if (score > highestScore) 
            {
                highestScore = score;
                winner = participant.getName();
            }
        }

        System.out.println("Winner: " + winner);
        scanner.close();
    }

    private static int calculateScore(List<Character> participantAnswers, Stack<Character> correctAnswers) 
    {
        int score = 0;
        for (int i = 0; i < participantAnswers.size(); i++) 
        {
            if (participantAnswers.get(i) == correctAnswers.get(i)) 
            {
                score++;
            }
        }
        return score;
    }
}

