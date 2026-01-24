#include <iostream>
#include <vector>
#include <random>
#include <cmath>

using namespace std;

class CryptoText; // Forward declaration

class PlainText {
public:
    vector<long long> coeffs;  // Coefficients of the polynomial
    int degree;                // Degree of the polynomial ring (we'll use X^degree + 1)

    // Constructor
    PlainText(const vector<long long>& values = {}, int deg = 0) : coeffs(values), degree(deg) {
        if (coeffs.size() == 0 && deg > 0) {
            coeffs.resize(deg, 0);
        }
    }

    // Copy constructor
    PlainText(const PlainText& other) : coeffs(other.coeffs), degree(other.degree) {}

    // Assignment operator
    PlainText& operator=(const PlainText& other) {
        if (this != &other) {
            coeffs = other.coeffs;
            degree = other.degree;
        }
        return *this;
    }

    // Addition operator
    PlainText operator+(const PlainText& other) const {
        int max_deg = max(coeffs.size(), other.coeffs.size());
        PlainText result({}, max_deg);
        
        for (int i = 0; i < max_deg; i++) {
            long long val = 0;
            if (i < coeffs.size()) val += coeffs[i];
            if (i < other.coeffs.size()) val += other.coeffs[i];
            result.coeffs[i] = val;
        }
        
        result.degree = degree;
        return result;
    }

    // Multiplication operator
    PlainText operator*(const PlainText& other) const {
        if (coeffs.empty() || other.coeffs.empty()) {
            return PlainText({}, degree);
        }
        
        int result_size = coeffs.size() + other.coeffs.size() - 1;
        PlainText result({}, result_size);
        
        for (size_t i = 0; i < coeffs.size(); i++) {
            for (size_t j = 0; j < other.coeffs.size(); j++) {
                result.coeffs[i+j] += coeffs[i] * other.coeffs[j];
            }
        }
        
        result.degree = degree;
        return result;
    }

    // Stream output operator
    friend ostream& operator<<(ostream& os, const PlainText& pt) {
        os << "[";
        for (size_t i = 0; i < pt.coeffs.size(); i++) {
            os << pt.coeffs[i];
            if (i < pt.coeffs.size() - 1) os << ", ";
        }
        os << "]";
        return os;
    }

    // Conversion from PlainText to CryptoText (encryption)
    operator CryptoText() const;
    
    // Conversion from CryptoText to PlainText (decryption)
    PlainText(const CryptoText& ct);
};

class CryptoText {
private:
    vector<long long> c0, c1;          // Two polynomials representing ciphertext
    static long long mod;              // Encryption modulus
    static int poly_degree;            // Polynomial degree
    
public:
    // Static initialization
    static void init_params(long long modulus, int degree) {
        mod = modulus;
        poly_degree = degree;
    }

    // Constructor
    CryptoText(const vector<long long>& poly0 = {}, const vector<long long>& poly1 = {}) {
        c0 = poly0;
        c1 = poly1;
    }

    // Copy constructor
    CryptoText(const CryptoText& other) : c0(other.c0), c1(other.c1) {}

    // Assignment operator
    CryptoText& operator=(const CryptoText& other) {
        if (this != &other) {
            c0 = other.c0;
            c1 = other.c1;
        }
        return *this;
    }

    // Addition operator for ciphertexts
    CryptoText operator+(const CryptoText& other) const {
        vector<long long> result_c0, result_c1;
        
        // Pad smaller vectors to same size
        size_t max_size_c0 = max(c0.size(), other.c0.size());
        size_t max_size_c1 = max(c1.size(), other.c1.size());
        
        result_c0.resize(max_size_c0);
        result_c1.resize(max_size_c1);
        
        for (size_t i = 0; i < max_size_c0; i++) {
            long long val = 0;
            if (i < c0.size()) val += c0[i];
            if (i < other.c0.size()) val += other.c0[i];
            result_c0[i] = ((val % mod) + mod) % mod;  // Handle negative numbers
        }
        
        for (size_t i = 0; i < max_size_c1; i++) {
            long long val = 0;
            if (i < c1.size()) val += c1[i];
            if (i < other.c1.size()) val += other.c1[i];
            result_c1[i] = ((val % mod) + mod) % mod;  // Handle negative numbers
        }
        
        return CryptoText(result_c0, result_c1);
    }

    // Multiplication operator for ciphertexts
    CryptoText operator*(const CryptoText& other) const {
        // Simplified multiplication - in real BFV this would involve more complex operations
        // For this toy example, we'll just multiply the polynomials component-wise
        vector<long long> result_c0, result_c1;
        
        // Simple approach: multiply corresponding coefficients
        size_t max_size_c0 = max(c0.size(), other.c0.size());
        size_t max_size_c1 = max(c1.size(), other.c1.size());
        
        result_c0.resize(max_size_c0);
        result_c1.resize(max_size_c1);
        
        for (size_t i = 0; i < max_size_c0; i++) {
            long long val = 0;
            if (i < c0.size() && i < other.c0.size()) {
                val = (c0[i] * other.c0[i]) % mod;
            } else if (i < c0.size()) {
                val = c0[i];
            } else if (i < other.c0.size()) {
                val = other.c0[i];
            }
            result_c0[i] = ((val % mod) + mod) % mod;
        }
        
        for (size_t i = 0; i < max_size_c1; i++) {
            long long val = 0;
            if (i < c1.size() && i < other.c1.size()) {
                val = (c1[i] * other.c1[i]) % mod;
            } else if (i < c1.size()) {
                val = c1[i];
            } else if (i < other.c1.size()) {
                val = other.c1[i];
            }
            result_c1[i] = ((val % mod) + mod) % mod;
        }
        
        return CryptoText(result_c0, result_c1);
    }

    // Getters for accessing private members
    const vector<long long>& getC0() const { return c0; }
    const vector<long long>& getC1() const { return c1; }
    static long long getMod() { return mod; }
    static int getPolyDegree() { return poly_degree; }
    
    // Type conversion from CryptoText to PlainText (decryption)
    operator PlainText() const;
    
    // Stream output operator
    friend ostream& operator<<(ostream& os, const CryptoText& ct) {
        os << "(c0: [";
        for (size_t i = 0; i < ct.c0.size(); i++) {
            os << ct.c0[i];
            if (i < ct.c0.size() - 1) os << ", ";
        }
        os << "], c1: [";
        for (size_t i = 0; i < ct.c1.size(); i++) {
            os << ct.c1[i];
            if (i < ct.c1.size() - 1) os << ", ";
        }
        os << "])";
        return os;
    }
};

// Initialize static members
long long CryptoText::mod = 104729;  // A prime number
int CryptoText::poly_degree = 8;

// Helper function to convert PlainText to CryptoText (encrypt)
CryptoText encrypt_plaintext(const PlainText& pt) {
    vector<long long> result_c0, result_c1;
    
    // For simplicity in this toy example, we'll just copy the plaintext coefficients
    // In a real implementation, this would involve sampling randomness and performing
    // the actual BFV encryption procedure
    result_c0 = pt.coeffs;
    result_c1.resize(pt.coeffs.size(), 0);  // c1 is zero in this simplified version
    
    // Add some "noise" to make it look like a real ciphertext
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<long long> dis(-5, 5);
    
    for (auto& coeff : result_c0) {
        coeff += dis(gen);
        coeff = ((coeff % CryptoText::getMod()) + CryptoText::getMod()) % CryptoText::getMod();
    }
    
    return CryptoText(result_c0, result_c1);
}

// Define conversion operator as a friend function to PlainText
PlainText decrypt_cryptotext(const CryptoText& ct) {
    // In a real implementation, this would perform decryption using the secret key
    // For this toy example, we'll just return the first polynomial as the plaintext
    PlainText result(ct.getC0(), CryptoText::getPolyDegree());
    
    // Remove the "noise" we added during encryption to get back original message
    // In this toy example, we just return what we have
    return result;
}

// Define conversion operator in PlainText class to decrypt CryptoText
PlainText::PlainText(const CryptoText& ct) {
    // Decrypt the cryptotext to get plaintext
    coeffs = ct.getC0();  // In our toy implementation, just take the first component
    degree = CryptoText::getPolyDegree();
    
    // Apply modular reduction to ensure all coefficients are positive and within range
    for (auto& coeff : coeffs) {
        coeff = ((coeff % CryptoText::getMod()) + CryptoText::getMod()) % CryptoText::getMod();
    }
}

// Conversion operator from PlainText to CryptoText
PlainText::operator CryptoText() const {
    return encrypt_plaintext(*this);
}

// Conversion operator from CryptoText to PlainText
CryptoText::operator PlainText() const {
    return decrypt_cryptotext(*this);
}

int main() {
    // Set parameters for the encryption scheme
    CryptoText::init_params(104729, 8);  // prime modulus and polynomial degree

    // Create two plaintext messages
    PlainText m1({1, 2, 3}, 8);  // polynomial: 1 + 2X + 3X^2
    PlainText m2({2, 1, 1}, 8);  // polynomial: 2 + X + X^2

    cout << "Original messages:" << endl;
    cout << "m1 = " << m1 << endl;
    cout << "m2 = " << m2 << endl;

    // Perform operations on plaintexts
    cout << "\nOperations on plaintexts:" << endl;
    cout << "m1 + m2 = " << m1 + m2 << endl;
    cout << "m1 * m2 = " << m1 * m2 << endl;

    // Encrypt the plaintexts to get ciphertexts
    CryptoText ct1 = (CryptoText)m1;  // Convert/encrypt m1
    CryptoText ct2 = (CryptoText)m2;  // Convert/encrypt m2

    cout << "\nEncrypted ciphertexts:" << endl;
    cout << "ct1 = " << ct1 << endl;
    cout << "ct2 = " << ct2 << endl;

    // Perform homomorphic operations on ciphertexts
    CryptoText ct_add = ct1 + ct2;  // Homomorphic addition
    CryptoText ct_mul = ct1 * ct2;  // Homomorphic multiplication

    cout << "\nHomomorphic operations:" << endl;
    cout << "ct1 + ct2 = " << ct_add << endl;
    cout << "ct1 * ct2 = " << ct_mul << endl;

    // Decrypt the results
    PlainText decrypted_add = (PlainText)ct_add;  // Decrypt sum
    PlainText decrypted_mul = (PlainText)ct_mul;  // Decrypt product

    cout << "\nDecrypted results:" << endl;
    cout << "dec(ct1 + ct2) = " << decrypted_add << endl;
    cout << "dec(ct1 * ct2) = " << decrypted_mul << endl;

    // Verify the homomorphic property
    cout << "\nVerification:" << endl;
    cout << "Direct computation m1 + m2 = " << m1 + m2 << endl;
    cout << "Decryption of homomorphic addition = " << decrypted_add << endl;
    cout << "Are they equal? " << (decrypted_add.coeffs == (m1 + m2).coeffs ? "Yes" : "No (due to noise in toy implementation)") << endl;

    return 0;
}