import React from 'react'
import Item from "./Item"

const ItemList = ({items}) => {
items.map((item) => <Item item={item} key={item.id} />);
  return (
    <section class="item-list">
        <h2>購入予定の商品</h2>
        {items.map((item) => (
        <Item item={item} key={item.id} />
      ))}
        <div class="total-amount">
            <span>合計金額: </span><span id="total">0</span>円
        </div>
    </section>
  )
}

export default ItemList
